#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load CandidateContest and related models with data scraped from the CAL-ACCESS website.
"""
import re
from datetime import date
from django.utils import timezone
from calaccess_processed import special_elections
from calaccess_processed.management.commands import LoadOCDModelsCommand

# Database utilities
from django.db.models import (
    IntegerField,
    CharField,
    Case,
    When,
    Q,
    Value,
)
from django.db.models.functions import Cast, Concat

# Models
from calaccess_scraped.models import (
    CandidateElection as ScrapedCandidateElection,
    IncumbentElection as ScrapedIncumbentElection,
)
from calaccess_processed.models import Form501Filing
from opencivicdata.core.models import Membership, Organization
from opencivicdata.elections.models import Election, CandidateContest


class Command(LoadOCDModelsCommand):
    """
    Load CandidateContest and related models with data scraped from the CAL-ACCESS website.
    """
    help = 'Load CandidateContest and related models with data scraped from the CAL-ACCESS website'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.header("Load Candidate Contests")
        self.load()

        # connect runoffs to their previously undecided contests
        if self.verbosity > 2:
            self.log(' Linking runoffs to previous contests')
        runoff_contests_q = CandidateContest.objects.filter(
            name__contains='RUNOFF'
        )
        for runoff in runoff_contests_q.all():
            previous_contest = self.find_previous_undecided_contest(runoff)
            if previous_contest:
                runoff.runoff_for_contest = previous_contest
                runoff.save()

        self.success("Done!")

    def parse_election_name(self, election_name):
        """
        Parse a scraped candidate election name into its constituent parts.

        Parts include:
        * Four-digit year (int)
        * Type (str), e.g., "GENERAL", "PRIMARY", "SPECIAL ELECTION", "SPECIAL RUNOFF")
        * Office (optional str)
        * District (optional int)

        Returns a dict.
        """
        pattern = r'^(?P<year>\d{4}) (?P<type>\b(?:[A-Z]| )+)(?: \((?P<office>(?:[A-Z]| )+)(?P<district>\d+)?\))?$' # NOQA
        parsed_name = re.match(pattern, election_name).groupdict()
        parsed_name['year'] = int(parsed_name['year'])
        parsed_name['type'] = parsed_name['type'].strip()
        if parsed_name['office']:
            parsed_name['office'] = parsed_name['office'].strip()
        if parsed_name['district']:
            parsed_name['district'] = int(parsed_name['district'])

        return parsed_name

    def lookup_election_date_from_name(self, election_name):
        """
        Use a scraped candidate election name to look up the election date.

        Return a timezone aware date object, if found, else None.
        """
        if election_name in (x[0] for x in special_elections.names_to_dates):
            date = dict(special_elections.names_to_dates)[election_name]
            date_obj = timezone.datetime.strptime(date, '%Y-%m-%d').date()
        else:
            # if not in the hard-coded list above, check the scraped
            # incumbent elections.
            parsed_name = self.parse_election_name(election_name)
            incumbent_elections_q = ScrapedIncumbentElection.objects.filter(
                date__year=parsed_name['year'],
                name__icontains=parsed_name['type'],
            )
            if incumbent_elections_q.count() == 1:
                date_obj = incumbent_elections_q[0].date
            else:
                try:
                    date_obj = self.get_regular_election_date(
                        parsed_name['year'],
                        parsed_name['type'],
                    )
                except:
                    date_obj = None

        return date_obj

    def get_or_create_election_from_name(self, election_name):
        """
        Use the scraped candidate election name to match an OCD Election.

        Returns a tuple (Election object, created), where created is a boolean
        specifying whether a Election was created.
        """
        parsed_name = self.parse_election_name(election_name)

        # Avoid conflating the Feb 2008 Primary with the Jun 2008 Primary
        if election_name == '2008 PRIMARY':
            try:
                ocd_election = Election.objects.get(
                    name=election_name,
                    date=date(2008, 6, 3),
                )
            except Election.DoesNotExist:
                ocd_election = self.create_election(
                    election_name,
                    date(2008, 6, 3),
                )
                created = True
            else:
                created = False
        # See if we can use the name to look up the election date
        elif self.lookup_election_date_from_name(election_name):
            date_obj = self.lookup_election_date_from_name(election_name)
            # Now that we have a date, get or create the Election
            try:
                ocd_election = Election.objects.get(date=date_obj)
            except Election.DoesNotExist:
                ocd_election = self.create_election(
                    '{year} {type}'.format(**parsed_name),
                    date_obj,
                )
                created = True
            else:
                created = False
                # if election already exists and is named 'SPECIAL' or
                # 'RECALL'
                if (
                    'SPECIAL' in ocd_election.name.upper() or
                    'RECALL' in ocd_election.name.upper()
                ):
                    # and the provided election_name includes either 'GENERAL'
                    # or 'PRIMARY'...
                    if (
                        re.match(r'^\d{4} GENERAL$', election_name) or
                        re.match(r'^\d{4} PRIMARY$', election_name)
                    ):
                        # update the name
                        ocd_election.name = election_name
                        ocd_election.save()
        # If lookup by name fails, raise an exception.
        else:
            raise Exception(
                "Could not match or find date for %s." % election_name
            )
        return (ocd_election, created)

    def get_form501_filing(self, scraped_candidate):
        """
        Return a Form501Filing that matches the scraped Candidate.

        By default, return the latest Form501FilingVersion, unless earliest
        is set to True.

        If the scraped Candidate has a scraped_id, lookup the Form501Filing
        by filer_id. Otherwise, lookup using the candidate's name.

        Return None can't match to a single Form501Filing.
        """
        election_data = self.parse_election_name(
            scraped_candidate.election.name,
        )
        office_data = self.parse_office_name(
            scraped_candidate.office_name,
        )

        # filter all form501 lookups by office type, district and election year
        # get the most recently filed Form501 within the election_year
        q = Form501Filing.objects.filter(
            office__iexact=office_data['type'],
            district=office_data['district'],
            election_year__lte=election_data['year'],
        )

        if scraped_candidate.scraped_id != '':
            try:
                # first, try to get w/ filer_id and election_type
                form501 = q.filter(
                    filer_id=scraped_candidate.scraped_id,
                    election_type=election_data['type'],
                ).latest('date_filed')
            except Form501Filing.DoesNotExist:
                # if that fails, try dropping election_type from filter
                try:
                    form501 = q.filter(
                        filer_id=scraped_candidate.scraped_id,
                    ).latest('date_filed')
                except Form501Filing.DoesNotExist:
                    form501 = None
        else:
            # if no filer_id, combine name fields from form501
            # first try "<last_name>, <first_name>" format.
            q = q.annotate(
                full_name=Concat(
                    'last_name',
                    Value(', '),
                    'first_name',
                    output_field=CharField(),
                )
            )
            # check if there are any with the "<last_name>, <first_name>"
            if not q.filter(full_name=scraped_candidate.name).exists():
                # use "<last_name>, <first_name> <middle_name>" format
                q = q.annotate(
                    full_name=Concat(
                        'last_name',
                        Value(', '),
                        'first_name',
                        Value(' '),
                        'middle_name',
                        output_field=CharField(),
                    ),
                )

            try:
                # first, try to get w/ filer_id and election_type
                form501 = q.filter(
                    full_name=scraped_candidate.name,
                    election_type=election_data['type'],
                ).latest('date_filed')
            except Form501Filing.DoesNotExist:
                # if that fails, try dropping election_type from filter
                try:
                    form501 = q.filter(
                        full_name=scraped_candidate.name,
                    ).latest('date_filed')
                except Form501Filing.DoesNotExist:
                    form501 = None

        return form501

    def get_or_create_contest(self, scraped_candidate, ocd_election, party=None):
        """
        Get or create an OCD CandidateContest object using  and Election object.

        Returns a tuple (CandidateContest object, created), where created is a boolean
        specifying whether a CandidateContest was created.
        """
        office_name = scraped_candidate.office_name
        post, post_created = self.get_or_create_post(office_name)

        # Assume all "SPECIAL" candidate elections are for contests where the
        # previous term of the office was unexpired.
        if 'SPECIAL' in scraped_candidate.election.name:
            previous_term_unexpired = True
            scraped_election = scraped_candidate.election.name
            election_type = self.parse_election_name(scraped_election)['type']
            contest_name = '{0} ({1})'.format(office_name, election_type)
        else:
            previous_term_unexpired = False
            if party:
                if party.name == 'UNKNOWN':
                    contest_name = '{0} ({1} PARTY)'.format(office_name, party.name)
                else:
                    contest_name = '{0} ({1})'.format(office_name, party.name)
            else:
                contest_name = office_name

        contest, contest_created = CandidateContest.objects.get_or_create(
            election=ocd_election,
            name=contest_name,
            previous_term_unexpired=previous_term_unexpired,
            party=party,
            division=post.division,
        )

        # if contest was created, add the Post
        if contest_created:
            contest.posts.create(
                post=post,
            )

        # always update the source for the contest
        contest.sources.update_or_create(
            url=scraped_candidate.url,
            note='Last scraped on {dt:%Y-%m-%d}'.format(
                dt=scraped_candidate.last_modified,
            )
        )

        return (contest, contest_created)

    def add_scraped_candidate_to_election(self, scraped_candidate, ocd_election):
        """
        Convert scraped_candidate to a Candidacy and add to ocd_election.

        Return a candidacy object.
        """
        # get the candidate's form501
        form501 = self.get_form501_filing(scraped_candidate)

        party = self.lookup_candidate_party_correction(
            scraped_candidate.name,
            ocd_election.date.year,
            self.parse_election_name(scraped_candidate.election.name)['type'],
            scraped_candidate.office_name,
        )

        if scraped_candidate.office_name == 'SUPERINTENDENT OF PUBLIC INSTRUCTION':
            party = Organization.objects.get(name="NO PARTY PREFERENCE")
        elif form501 and not party:
            party = self.lookup_party(form501.party)
            if not party:
                party = self.get_party_for_filer_id(
                    int(form501.filer_id),
                    ocd_election.date,
                )
        elif scraped_candidate.scraped_id != '':
            party = self.get_party_for_filer_id(
                int(scraped_candidate.scraped_id),
                ocd_election.date,
            )
        else:
            party = None

        # if it's a primary election before 2012 for an office other than
        # superintendent of public instruction, include party in
        # get_or_create_contest criteria (if we have a party)
        if (
            'PRIMARY' in scraped_candidate.election.name and
            ocd_election.date.year < 2012 and
            scraped_candidate.office_name != 'SUPERINTENDENT OF PUBLIC INSTRUCTION'
        ):
            if not party:
                # use UNKNOWN party
                party = Organization.objects.get(identifiers__identifier=16011)

            contest, contest_created = self.get_or_create_contest(
                scraped_candidate,
                ocd_election,
                party=party,
            )
        else:
            contest, contest_created = self.get_or_create_contest(
                scraped_candidate,
                ocd_election,
            )

        if contest_created and self.verbosity > 2:
            self.log(' Created new CandidateContest: %s' % contest.name)

        # default status for scraped candidates
        registration_status = 'qualified'

        # http://www.sos.ca.gov/elections/prior-elections/statewide-election-results/primary-election-march-7-2000/certified-list-candidates/ # noqa
        if scraped_candidate.name == 'COURTRIGHT DONNA':
            scraped_candidate_name = 'COURTRIGHT, DONNA'
        else:
            scraped_candidate_name = scraped_candidate.name

        candidacy, candidacy_created = self.get_or_create_candidacy(
            contest,
            scraped_candidate_name,
            registration_status,
            filer_id=scraped_candidate.scraped_id,
        )

        if candidacy_created and self.verbosity > 2:
            template = ' Created new Candidacy: {0.candidate_name} in {0.post.label}'
            self.log(template.format(candidacy))

        # add extra data from form501, if available
        if form501:
            self.link_form501_to_candidacy(form501.filing_id, candidacy)
            self.update_candidacy_from_form501s(candidacy)

            # if the scraped_candidate lacks a filer_id, add the
            # Form501Filing.filer_id
            if scraped_candidate.scraped_id == '':
                candidacy.person.identifiers.get_or_create(
                    scheme='calaccess_filer_id',
                    identifier=form501.filer_id,
                )
        if party and not candidacy.party:
            candidacy.party = party
            candidacy.save()

        # always update the source for the candidacy
        candidacy.sources.update_or_create(
            url=scraped_candidate.url,
            note='Last scraped on {dt:%Y-%m-%d}'.format(
                dt=scraped_candidate.last_modified,
            )
        )

        return candidacy

    def check_incumbent_status(self, candidacy):
        """
        Check if the Candidacy is for the incumbent officeholder.

        Return True if:
        * Membership exists for the Person and Post linked to the Candidacy, and
        * Membership.end_date is NULL or has a year later than Election.date.year.
        """
        incumbent_q = Membership.objects.filter(
            post=candidacy.post,
            person=candidacy.person,
        ).annotate(
            # Cast end_date's value as an int, treat '' as NULL
            end_year=Cast(
                Case(When(end_date='', then=None)),
                IntegerField(),
            )
        ).filter(
            Q(end_year__gt=candidacy.election.date.year) |
            Q(end_date='')
        )
        if incumbent_q.exists():
            is_incumbent = True
        else:
            is_incumbent = False

        return is_incumbent

    def get_ocd_election(self, scraped_election):
        """
        Get and OCD Election from scraped_election.
        """
        # try looking up the election using the scraped id
        try:
            ocd_election = Election.objects.filter(
                identifiers__scheme='calaccess_election_id',
                identifiers__identifier=scraped_election.scraped_id,
            ).get()
        except Election.DoesNotExist:
            ocd_election, elec_created = self.get_or_create_election_from_name(
                scraped_election.name,
            )
            if elec_created and self.verbosity > 2:
                self.log(' Created new Election: %s' % ocd_election.name)
            # Add the missing identifier
            ocd_election.identifiers.create(
                scheme='calaccess_election_id',
                identifier=scraped_election.scraped_id,
            )

        # Whether Election is new or not, update EventSource
        ocd_election.sources.update_or_create(
            url=scraped_election.url,
            note='Last scraped on {dt:%Y-%m-%d}'.format(
                dt=scraped_election.last_modified,
            )
        )

        return ocd_election

    def find_previous_undecided_contest(self, runoff_contest):
        """
        Find the undecided contest that preceeded runoff_contest.
        """
        # Get the contest's post (should only ever be one per contest)
        post = runoff_contest.posts.all()[0].post

        # Then try getting the most recent contest for the same post
        # that preceeds the runoff contest
        try:
            contest = CandidateContest.objects.filter(
                posts__post=post,
                election__date__lt=runoff_contest.election.date,
            ).latest('election__date')
        except CandidateContest.DoesNotExist:
            contest = None

        return contest

    def load(self):
        """
        Load OCD Election, CandidateContest and related models with data scraped from CAL-ACCESS website.
        """
        # See if we should bother checking incumbent status
        members_are_loaded = Membership.objects.exists()

        # Loop over scraped_elections
        for scraped_election in ScrapedCandidateElection.objects.all():
            ocd_election = self.get_ocd_election(scraped_election)
            # then over candidates in the scraped_election
            for scraped_candidate in scraped_election.candidates.all():
                if self.verbosity > 2:
                    self.log(
                        ' Processing scraped Candidate.id %s' % scraped_candidate.id
                    )
                candidacy = self.add_scraped_candidate_to_election(
                    scraped_candidate,
                    ocd_election
                )
                # check incumbent status
                if members_are_loaded:
                    if self.check_incumbent_status(candidacy):
                        candidacy.is_incumbent = True
                        candidacy.save()
                        if self.verbosity > 2:
                            self.log(' Identified as incumbent.')
                        # set is_incumbent False for all other candidacies
                        contest = candidacy.contest
                        contest.candidacies.exclude(
                            is_incumbent=True
                        ).update(is_incumbent=False)
        return
