#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base classes for custom management commands.
"""
import os
import re
import csv
import logging
from datetime import date
from django.apps import apps
from django.utils import timezone
from django.db.models import Count, Q
from opencivicdata.merge import merge
from django.utils.termcolors import colorize
from calaccess_raw import get_download_directory
from django.core.management.base import BaseCommand
from django.core.management import call_command, CommandError
from opencivicdata.elections.models import Election, Candidacy
from calaccess_raw.models import RawDataVersion, FilerToFilerTypeCd
from opencivicdata.core.management.commands.loaddivisions import load_divisions
from calaccess_processed.models import ProcessedDataVersion, Form501FilingVersion
from opencivicdata.core.models import (
    Division,
    Jurisdiction,
    Organization,
    Person,
    Post,
)
logger = logging.getLogger(__name__)


class CalAccessCommand(BaseCommand):
    """
    Base class for all custom CalAccess-related management commands.
    """
    def handle(self, *args, **options):
        """
        Sets options common to all commands.

        Any command subclassing this object should implement its own
        handle method, as is standard in Django, and run this method
        via a super call to inherit its functionality.
        """
        # Set global options
        self.verbosity = options.get("verbosity")
        self.no_color = options.get("no_color")

        # Start the clock
        self.start_datetime = timezone.now()

        # set up processed data directory
        self.data_dir = get_download_directory()
        self.processed_data_dir = os.path.join(
            self.data_dir,
            'processed',
        )
        if not os.path.exists(self.processed_data_dir):
            # make the processed data director
            os.makedirs(self.processed_data_dir)
            # set permissions to allow other users to write and execute
            os.chmod(self.processed_data_dir, 0o703)

    def get_or_create_processed_version(self):
        """
        Get or create the current processed version.

        Return a tuple (ProcessedDataVersion object, created), where
        created is a boolean specifying whether a version was created.
        """
        # get the latest raw data version
        try:
            latest_raw_version = RawDataVersion.objects.latest(
                'release_datetime',
            )
        except RawDataVersion.DoesNotExist:
            raise CommandError(
                'No raw CAL-ACCESS data loaded (run `python manage.py '
                'updatecalaccessrawdata`).'
            )

        # check if latest raw version update completed
        if latest_raw_version.update_stalled:
            msg_tmp = 'Update to raw version released at %s did not complete'
            raise CommandError(
                msg_tmp % latest_raw_version.release_datetime.ctime()
            )

        return ProcessedDataVersion.objects.get_or_create(
            raw_version=latest_raw_version,
        )

    def header(self, string):
        """
        Writes out a string to stdout formatted to look like a header.
        """
        logger.debug(string)
        if not getattr(self, 'no_color', None):
            string = colorize(string, fg="cyan", opts=("bold",))
        self.stdout.write(string)

    def log(self, string):
        """
        Writes out a string to stdout formatted to look like a standard line.
        """
        logger.debug(string)
        if not getattr(self, 'no_color', None):
            string = colorize("%s" % string, fg="white")
        self.stdout.write(string)

    def success(self, string):
        """
        Writes out a string to stdout formatted green to communicate success.
        """
        logger.debug(string)
        if not getattr(self, 'no_color', None):
            string = colorize(string, fg="green")
        self.stdout.write(string)

    def warn(self, string):
        """
        Writes string to stdout formatted yellow to communicate a warning.
        """
        logger.warn(string)
        if not getattr(self, 'no_color', None):
            string = colorize(string, fg="yellow")
        self.stdout.write(string)

    def failure(self, string):
        """
        Writes string to stdout formatted red to communicate failure.
        """
        logger.error(string)
        if not getattr(self, 'no_color', None):
            string = colorize(string, fg="red")
        self.stdout.write(string)

    def duration(self):
        """
        Calculates how long command has been running and writes it to stdout.
        """
        duration = timezone.now() - self.start_datetime
        self.stdout.write('Duration: {}'.format(str(duration)))
        logger.debug('Duration: {}'.format(str(duration)))

    def __str__(self):
        return re.sub(r'(.+\.)*', '', self.__class__.__module__)


class LoadOCDModelsCommand(CalAccessCommand):
    """
    Base class for OCD model loading management commands.
    """
    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(LoadOCDModelsCommand, self).handle(*args, **options)
        try:
            self.state_division = Division.objects.get(
                id='ocd-division/country:us/state:ca'
            )
        except Division.DoesNotExist:
            if self.verbosity > 2:
                self.log(' CA state division missing. Loading all U.S. divisions')
            load_divisions('us')
            self.state_division = Division.objects.get(
                id='ocd-division/country:us/state:ca'
            )
        self.state_jurisdiction = Jurisdiction.objects.get_or_create(
            name='California State Government',
            url='http://www.ca.gov',
            division=self.state_division,
            classification='government',
        )[0]
        self.executive_branch = Organization.objects.get_or_create(
            name='California State Executive Branch',
            classification='executive',
        )[0]
        self.sos = Organization.objects.get_or_create(
            name='California Secretary of State',
            classification='executive',
            parent=self.executive_branch,
        )[0]

    def get_regular_election_date(self, year, election_type):
        """
        Get the date of the election in the given year and type.

        Raise an exception if year is not even or if election_type is not
        "PRIMARY" or "GENERAL".

        Return a date object.
        """
        # Rules defined here:
        # https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=ELEC&division=1.&title=&part=&chapter=1.&article= # noqa
        if year % 2 != 0:
            raise Exception("Regular elections occur in even years.")
        elif election_type.upper() == 'PRIMARY':
            # Primary elections are in June
            month = 6
        elif election_type.upper() == 'GENERAL':
            # General elections are in November
            month = 11
        else:
            raise Exception("election_type must 'PRIMARY' or 'GENERAL'.")

        # get the first weekday
        # zero-indexed starting with monday
        first_weekday = date(year, month, 1).weekday()
        # calculate day or first tuesday after first monday
        day_or_month = (7 - first_weekday) % 7 + 2

        return date(year, month, day_or_month)

    def create_election(self, name, date_obj):
        """
        Create an OCD Election object.
        """
        admin = Organization.objects.get_or_create(
            name='Elections Division',
            classification='executive',
            parent=self.sos,
        )[0]
        obj = Election.objects.create(
            date=date_obj,
            name=name,
            administrative_organization=admin,
            division=self.state_division,
        )
        return obj

    def parse_office_name(self, office_name):
        """
        Parse string containg the name for an office.

        Expected format is "{TYPE NAME}[{DISTRICT NUMBER}]".

        Return a dict with two keys: type and district.
        """
        office_pattern = r'^(?P<type>[A-Z ]+)(?P<district>\d{2})?$'
        try:
            parsed = re.match(office_pattern, office_name.upper()).groupdict()
        except AttributeError:
            parsed = {'type': None, 'district': None}
        else:
            parsed['type'] = parsed['type'].strip()
            try:
                parsed['district'] = int(parsed['district'])
            except TypeError:
                pass

        return parsed

    def get_or_create_post(self, office_name, get_only=False):
        """
        Get or create a Post object with an office_name string.

        Returns a tuple (Post object, created), where created is a boolean
        specifying whether a Post was created.
        """
        parsed_office = self.parse_office_name(office_name)

        # prepare to get or create post
        raw_post = {'label': office_name.title().replace('Of', 'of')}

        if parsed_office['type'] == 'STATE SENATE':
            raw_post['division'] = Division.objects.get(
                subid1='ca',
                subtype2='sldu',
                subid2=str(parsed_office['district']),
            )
            raw_post['organization'] = Organization.objects.get_or_create(
                name='California State Senate',
                classification='upper',
            )[0]
            raw_post['role'] = 'Senator'
        elif parsed_office['type'] == 'ASSEMBLY':
            raw_post['division'] = Division.objects.get(
                subid1='ca',
                subtype2='sldl',
                subid2=str(parsed_office['district']),
            )
            raw_post['organization'] = Organization.objects.get_or_create(
                name='California State Assembly',
                classification='lower',
            )[0]
            raw_post['role'] = 'Assembly Member'
        else:
            # If not Senate or Assembly, assume this is a state office
            raw_post['division'] = self.state_division
            if parsed_office['type'] == 'MEMBER BOARD OF EQUALIZATION':
                raw_post['organization'] = Organization.objects.get_or_create(
                    name='State Board of Equalization',
                    parent=self.executive_branch,
                )[0]
                raw_post['role'] = 'Board Member'
            elif parsed_office['type'] == 'SECRETARY OF STATE':
                raw_post['organization'] = self.sos
                raw_post['role'] = raw_post['label']
            else:
                raw_post['organization'] = self.executive_branch
                raw_post['role'] = raw_post['label']

        if get_only:
            post_created = False
            try:
                post = Post.objects.get(**raw_post)
            except Post.DoesNotExist:
                post = None
        else:
            post, post_created = Post.objects.get_or_create(**raw_post)

        return post, post_created

    def get_or_create_person(self, sort_name, filer_id=None):
        """
        Get or create a Person object with the name string and optional filer_id.

        If a filer_id is provided, first attempt to lookup the Person by filer_id.
        If matched, and the provided name doesn't match the current name of the Person
        and isn't included in the other names of the Person, add it as an other_name.

        If the person doesn't exist (or the filer_id is not provided), create a
        new Person.

        Returns a tuple (Person object, created), where created is a boolean
        specifying whether a Person was created.
        """
        split_name = sort_name.split(',')
        split_name.reverse()
        name = ' '.join(split_name).strip()
        person = None
        created = False

        if filer_id:
            if filer_id != '':
                try:
                    person = Person.objects.get(
                        identifiers__scheme='calaccess_filer_id',
                        identifiers__identifier=filer_id,
                    )
                except Person.DoesNotExist:
                    pass
                else:
                    if (
                        person.name != name and
                        not person.other_names.filter(name=name).exists()
                    ):
                        person.other_names.create(
                            name=name,
                            note='Matched on calaccess_filer_id'
                        )
        if not person:
            # split and flip the original name string
            split_name = name.split(',').reverse()
            person = Person.objects.create(
                name=name,
                sort_name=sort_name,
            )
            if filer_id:
                person.identifiers.create(
                    scheme='calaccess_filer_id',
                    identifier=filer_id,
                )
            created = True

        return (person, created)

    def get_or_create_candidacy(self, contest_obj, sort_name, registration_status, filer_id=None):
        """
        Get or create a Candidacy object.

        First, try getting an existing Candidacy within the given CandidateContest
        linked to a Person with the provided filer_id. If matched and the matched Person
        has different current name and doesn't have the provided name as an other name,
        add the other name.

        Next, try getting an existing Candidacy within the given CandidateContest
        linked to a Person with provided name (as default name or other name). If
        matched and match candidate doesn't already have filer_id, add the filer_id.

        If no match or if the matched person already has a different filer_id, create
        a new Candidacy (this may also create a new Person record).

        Returns a tuple (Candidacy object, created), where created is a boolean
        specifying whether a Candidacy was created.
        """
        split_name = sort_name.split(',')
        split_name.reverse()
        name = ' '.join(split_name).strip()
        candidacy = None

        # first, try matching to existing candidate in contest with filer_id
        if filer_id:
            try:
                candidacy = contest_obj.candidacies.get(
                    person__identifiers__scheme='calaccess_filer_id',
                    person__identifiers__identifier=filer_id,
                )
            except Candidacy.DoesNotExist:
                pass
            else:
                candidacy_created = False
                # if provided name not person's current name and not linked to person
                # add it
                if (
                    candidacy.person.name != name and
                    not candidacy.person.other_names.filter(name=name).exists()
                ):
                    candidacy.person.other_names.create(
                        name=name,
                        note='Matched on CandidateContest and calaccess_filer_id'
                    )
        # if filer_id match fails (or no filer_id), try matching to candidate
        # in contest with provided name
        if not candidacy:
            try:
                candidacy = contest_obj.candidacies.get(
                    Q(candidate_name=name) |
                    Q(person__name=name) |
                    Q(person__other_names__name=name)
                )
            except Candidacy.MultipleObjectsReturned:
                # weird case when someone filed for the same race
                # with three different filer_ids
                if sort_name == 'MC NEA, DOUGLAS A.':
                    candidacy = None
            except Candidacy.DoesNotExist:
                pass
            else:
                candidacy_created = False
                # if filer_id provided
                if filer_id:
                    # check to make sure candidate with same name doesn't have
                    # diff filer_id
                    has_diff_filer_id = candidacy.person.identifiers.filter(
                        scheme='calaccess_filer_id',
                    ).exists()
                    if has_diff_filer_id:
                        # if so, don't conflate
                        candidacy = None
                    else:
                        # add filer_id to existing candidate
                        candidacy.person.identifiers.create(
                            scheme='calaccess_filer_id',
                            identifier=filer_id,
                        )
        # if no matched candidate yet, make a new one
        if not candidacy:
            candidacy_created = True
            person, person_created = self.get_or_create_person(
                sort_name,
                filer_id=filer_id,
            )
            if person_created and self.verbosity > 2:
                self.log(' Created new Person: %s' % person.name)

            # if provided name not person's current name or other_name
            if (
                person.name != name and
                not person.other_names.filter(name=name).exists()
            ):
                person.other_names.create(
                    name=name,
                    note='From %s candidacy' % contest_obj
                )

            candidacy = contest_obj.candidacies.create(
                person=person,
                post=contest_obj.posts.all()[0].post,
                candidate_name=name,
                registration_status=registration_status,
            )

        # if provided registration does not equal the default, update
        if registration_status != 'filed':
            candidacy.registration_status = registration_status
            candidacy.save()

        return (candidacy, candidacy_created)

    def link_form501_to_candidacy(self, form501_id, candidacy_obj):
        """
        Link a Form501Filing to a Candidacy, if it isn't already.
        """
        if 'form501_filing_ids' in candidacy_obj.extras:
            if form501_id not in candidacy_obj.extras['form501_filing_ids']:
                candidacy_obj.extras['form501_filing_ids'].append(form501_id)
        else:
            candidacy_obj.extras['form501_filing_ids'] = [form501_id]

        candidacy_obj.save()

        return

    def update_candidacy_from_form501s(self, candidacy_obj):
        """
        Set Candidacy fields using data extracted from linked Form501Filings.
        """
        # get all Form501FilingVersions linked to Candidacy
        filing_ids = candidacy_obj.extras['form501_filing_ids']
        filings = Form501FilingVersion.objects.filter(filing_id__in=filing_ids)

        # keep the earliest filed_date
        first_filed_date = filings.earliest('date_filed').date_filed

        if candidacy_obj.filed_date != first_filed_date:
            candidacy_obj.filed_date = first_filed_date
            candidacy_obj.save()

        # keep if latest filing says withdrawn
        latest = filings.latest('date_filed')
        if latest.statement_type == '10003':
            if candidacy_obj.registration_status != 'withdrawn':
                candidacy_obj.registration_status = 'withdrawn'

        candidacy_obj.save()

        return

    def lookup_candidate_party_correction(
        self,
        candidate_name,
        year,
        election_type,
        office
    ):
        """
        Return the correct party for a given candidate name, year, election_type and office.

        Return None if no correction found.
        """
        # Get the path to our corrections file
        app = apps.get_app_config("calaccess_processed")
        module_dir = os.path.abspath(os.path.dirname(app.module.__file__))
        corrections_path = os.path.join(module_dir, 'corrections', "candidate_party.csv")

        # Open up the corrections
        corrections = csv.DictReader(open(corrections_path, 'r'))

        # Filter down to the ones we've corrected
        corrections = [d for d in corrections if d['party']]

        # Filter down to the ones that match
        matches = [
            d['party'] for d in corrections if (
                d['candidate_name'] == candidate_name and
                d['year'] == year and
                d['election_type'] == election_type and
                d['office'] == office
            )
        ]

        # If there's more than one result throw an error
        if len(matches) > 1:
            raise Exception('More than one correction found.')
        # If there's no match return None
        elif len(matches) == 0:
            return None
        # If there's only one match return that
        else:
            return matches[0]

    def lookup_party(self, party):
        """
        Return an Organization with a name or abbreviation that matches party.

        If none found, return the "UKNOWN" Organization.
        """
        if not Organization.objects.filter(classification='party').exists():
            if self.verbosity > 2:
                self.log(" No parties loaded.")
            call_command(
                'loadparties',
                verbosity=self.verbosity,
                no_color=self.no_color,
            )

        party_q = Organization.objects.filter(classification='party')

        try:
            # first by full name
            party = party_q.get(name=party)
        except Organization.DoesNotExist:
            # then try an alternate name
            try:
                # then try alternate names
                party = Organization.objects.get(
                    other_names__name=party,
                )
            except Organization.DoesNotExist:
                party = Organization.objects.get(name='UNKNOWN')

        return party

    def get_party_for_filer_id(self, filer_id, election_date):
        """
        Lookup the party for the given filer_id, effective before election_date.

        If not found, return the "UNKNOWN" Organization object.
        """
        try:
            party_cd = FilerToFilerTypeCd.objects.filter(
                filer_id=filer_id,
                effect_dt__lte=election_date,
            ).latest('effect_dt').party_cd
        except FilerToFilerTypeCd.DoesNotExist:
            party = Organization.objects.get(name='UNKNOWN')
        else:
            # transform "INDEPENDENT" and "NON-PARTISAN" to "NO PARTY PREFERENCE"
            if party_cd in [16007, 16009]:
                party_cd = 16012
            try:
                party = Organization.objects.get(identifiers__identifier=party_cd)
            except Organization.DoesNotExist:
                party = Organization.objects.get(name='UNKNOWN')

        return party

    def merge_persons(self, persons):
        """
        Merge items in persons iterable into one Person object.

        Return the merged Person object.
        """
        # each person will be merged into this one
        keep = persons.pop(0)

        # loop over all the rest
        for i in persons:
            merge(keep, i)
            keep.refresh_from_db()

        # also delete the now duplicated PersonIdentifier objects
        keep_filer_ids = keep.identifiers.filter(scheme='calaccess_filer_id')

        dupe_filer_ids = keep_filer_ids.values("identifier").annotate(
            row_count=Count('id'),
        ).order_by().filter(row_count__gt=1)

        for i in dupe_filer_ids.all():
            # delete all rows with that filer_id
            keep_filer_ids.filter(identifier=i['identifier']).delete()
            # then re-add the one
            keep.identifiers.create(
                scheme='calaccess_filer_id',
                identifier=i['identifier'],
            )

        # and dedupe candidacy records
        # first, make groups by contests with more than one candidacy
        contest_group_q = keep.candidacies.values("contest").annotate(
            row_count=Count('id')
        ).filter(row_count__gt=1)

        # loop over each contest group
        for group in contest_group_q.all():
            cands = keep.candidacies.filter(contest=group['contest'])
            # preference to "qualified" candidacy (from scrape)
            if cands.filter(registration_status='qualified').exists():
                cand_to_keep = cands.filter(registration_status='qualified').all()[0]
            # or the one with the most recent filed_date
            else:
                cand_to_keep = cands.latest('filed_date')

            # loop over all the other candidacy in the group
            for cand_to_discard in cands.exclude(id=cand_to_keep.id).all():
                # assuming the only thing in extras is form501_filing_ids
                if 'form501_filing_ids' in cand_to_discard.extras:
                    for i in cand_to_discard.extras['form501_filing_ids']:
                        self.link_form501_to_candidacy(i, cand_to_keep)
                cand_to_keep.refresh_from_db()

                if 'form501_filing_ids' in cand_to_keep.extras:
                    self.update_candidacy_from_form501s(cand_to_keep)
                cand_to_keep.refresh_from_db()

                # keep the candidate_name, if not already somewhere else
                if (
                    cand_to_discard.candidate_name != cand_to_keep.candidate_name and
                    cand_to_discard.candidate_name != cand_to_keep.person.name and
                    not cand_to_keep.person.other_names.filter(
                        name=cand_to_discard.candidate_name
                    ).exists()
                ):
                    keep.other_names.create(
                        name=cand_to_discard.candidate_name,
                        note='From merge of %s candidacies' % cand_to_keep.contest
                    )
                    cand_to_keep.refresh_from_db()

                # keep the candidacy sources
                if cand_to_discard.sources.exists():
                    for source in cand_to_discard.sources.all():
                        if not cand_to_keep.sources.filter(url=source.url).exists():
                            cand_to_keep.sources.create(
                                url=source.url,
                                note=source.note,
                            )
                        cand_to_keep.refresh_from_db()

                # keep earliest filed_date
                if cand_to_keep.filed_date and cand_to_discard.filed_date:
                    if cand_to_keep.filed_date > cand_to_discard.filed_date:
                        cand_to_keep.filed_date = cand_to_discard.filed_date
                elif cand_to_discard.filed_date:
                    cand_to_keep.filed_date = cand_to_discard.filed_date
                # keep is_incumbent if True
                if not cand_to_keep.is_incumbent and cand_to_discard.is_incumbent:
                    cand_to_keep.is_incumbent = cand_to_discard.is_incumbent
                # assuming not trying to merge candidacies with different parties
                if not cand_to_keep.party and cand_to_discard.party:
                    cand_to_keep.party = cand_to_discard.party

                cand_to_keep.save()
                cand_to_discard.delete()

        keep.refresh_from_db()
        return keep
