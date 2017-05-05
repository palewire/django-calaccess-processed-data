#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load CandidateContest and related models with data scraped from the CAL-ACCESS website.
"""
import re
from django.utils import timezone
from django.db.models import (
    IntegerField,
    CharField,
    Case,
    When,
    Q,
    Value,
)
from django.db.models.functions import Cast, Concat
from calaccess_processed.management.commands import LoadOCDModelsCommand
from calaccess_processed.models import (
    CandidateScrapedElection,
    IncumbentScrapedElection,
    Form501Filing,
)
from opencivicdata.models import (
    Election,
    ElectionIdentifier,
    CandidateContest,
    Membership,
    Party,
)


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
        self.load()
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

        Name to date mappings are hardcoded, compiled from CAL-ACCESS:
        http://cal-access.ss.ca.gov/Campaign/Candidates/

        And also the SoS site:
        * http://www.sos.ca.gov/elections/prior-elections/special-elections/
        * http://elections.cdn.sos.ca.gov/special-elections/pdf/special-elections-history.pdf

        Return a timezone aware date object, if found, else None.
        """
        election_dates = (
            ('2016 SPECIAL ELECTION (ASSEMBLY 31)', '2016-4-5'),
            ('2015 SPECIAL RUNOFF (STATE SENATE 07)', '2015-5-19'),
            ('2015 SPECIAL ELECTION (STATE SENATE 07)', '2015-3-17'),
            ('2015 SPECIAL ELECTION (STATE SENATE 21)', '2015-3-17'),
            ('2015 SPECIAL ELECTION (STATE SENATE 37)', '2015-3-17'),
            ('2014 SPECIAL ELECTION (STATE SENATE 35)', '2014-12-9'),
            ('2014 SPECIAL ELECTION (STATE SENATE 23)', '2014-3-25'),
            ('2013 SPECIAL ELECTION (ASSEMBLY 54)', '2013-12-3'),
            ('2013 SPECIAL RUNOFF (ASSEMBLY 45)', '2013-11-19'),
            ('2013 SPECIAL ELECTION (ASSEMBLY 45)', '2013-9-17'),
            ('2013 SPECIAL RUNOFF (ASSEMBLY 52)', '2013-9-24'),
            ('2013 SPECIAL ELECTION (ASSEMBLY 52)', '2013-7-23'),
            ('2013 SPECIAL ELECTION (STATE SENATE 26)', '2013-9-17'),
            ('2013 SPECIAL RUNOFF (STATE SENATE 16)', '2013-7-23'),
            ('2013 SPECIAL ELECTION (STATE SENATE 16)', '2013-5-21'),
            ('2013 SPECIAL ELECTION (ASSEMBLY 80)', '2013-5-21'),
            ('2013 SPECIAL RUNOFF (STATE SENATE 32)', '2013-5-14'),
            ('2013 SPECIAL ELECTION (STATE SENATE 32)', '2013-3-12'),
            ('2013 SPECIAL ELECTION (STATE SENATE 40)', '2013-3-12'),
            ('2013 SPECIAL ELECTION (STATE SENATE 04)', '2013-1-8'),
            ('2012 SPECIAL ELECTION (STATE SENATE 04)', '2012-11-6'),
            ('2011 SPECIAL RUNOFF (ASSEMBLY 04)', '2011-5-3'),
            ('2011 SPECIAL ELECTION (ASSEMBLY 04)', '2011-3-8'),
            ('2011 SPECIAL ELECTION (STATE SENATE 28)', '2011-2-15'),
            ('2011 SPECIAL ELECTION (STATE SENATE 17)', '2011-2-15'),
            ('2011 SPECIAL RUNOFF (STATE SENATE 01)', '2011-1-4'),
            ('2010 SPECIAL ELECTION (STATE SENATE 01)', '2010-11-2'),
            ('2010 SPECIAL RUNOFF (STATE SENATE 15)', '2010-8-17'),
            ('2010 SPECIAL ELECTION (STATE SENATE 15)', '2010-6-22'),
            ('2010 SPECIAL RUNOFF (STATE SENATE 37)', '2010-6-8'),
            ('2010 SPECIAL ELECTION (STATE SENATE 37)', '2010-4-13'),
            ('2010 SPECIAL RUNOFF (ASSEMBLY 43)', '2010-6-8'),
            ('2010 SPECIAL ELECTION (ASSEMBLY 43)', '2010-4-13'),
            ('2010 SPECIAL RUNOFF (ASSEMBLY 72)', '2010-1-12'),
            ('2009 SPECIAL ELECTION (ASSEMBLY 72)', '2009-11-17'),
            ('2009 SPECIAL ELECTION (ASSEMBLY 51)', '2009-9-1'),
            ('2009 SPECIAL RUNOFF (STATE SENATE 26)', '2009-5-19'),
            ('2009 SPECIAL ELECTION (STATE SENATE 26)', '2009-3-24'),
            ('2008 SPECIAL RUNOFF (ASSEMBLY 55)', '2008-2-5'),
            ('2007 SPECIAL ELECTION (ASSEMBLY 55)', '2007-12-11'),
            ('2007 SPECIAL ELECTION (ASSEMBLY 39)', '2007-5-15'),
            ('2006 SPECIAL RUNOFF (STATE SENATE 35)', '2006-6-6'),
            ('2006 SPECIAL ELECTION (STATE SENATE 35)', '2006-4-11'),
            ('2005 SPECIAL ELECTION (ASSEMBLY 53)', '2005-9-13'),
            ('2003 SPECIAL ELECTION (GOVERNOR)', '2003-10-7'),
            ('2001 SPECIAL ELECTION (ASSEMBLY 49)', '2001-5-15'),
            ('2001 SPECIAL RUNOFF (ASSEMBLY 65)', '2001-2-6'),
            ('2001 SPECIAL ELECTION (ASSEMBLY 65)', '2001-4-3'),
            ('2001 SPECIAL ELECTION (STATE SENATE 24)', '2001-3-26'),
        )

        if election_name in (x[0] for x in election_dates):
            date = dict(election_dates)[election_name]
            date_obj = timezone.make_aware(
                timezone.datetime.strptime(
                    date,
                    '%Y-%m-%d',
                )
            )
        else:
            date_obj = None

        return date_obj

    def get_or_create_election_from_name(self, election_name):
        """
        Use the scraped candidate election name to match an OCD Election.

        Returns a tuple (Election object, created), where created is a boolean
        specifying whether a Election was created.
        """
        parsed_name = self.parse_election_name(election_name)

        ocd_elections_q = Election.objects.filter(
            start_time__year=parsed_name['year'],
            name__icontains=parsed_name['type'],
        )
        incumbent_elections_q = IncumbentScrapedElection.objects.filter(
            date__year=parsed_name['year'],
            name__icontains=parsed_name['type'],
        )

        if election_name == '2008 PRIMARY':
            try:
                ocd_elec = Election.objects.get(
                    name=election_name,
                    start_time=timezone.datetime(2008, 6, 3, 0, 0, tzinfo=timezone.utc),
                )
            except Election.DoesNotExist:
                ocd_elec = self.create_election(
                    election_name,
                    timezone.datetime(2008, 6, 3, 0, 0, tzinfo=timezone.utc),
                )
                created = True
            else:
                created = False
        elif ocd_elections_q.count() == 1:
            ocd_elec = ocd_elections_q[0]
            created = False
        else:
            if self.lookup_election_date_from_name(election_name):
                date_obj = self.lookup_election_date_from_name(election_name)
            elif incumbent_elections_q.count() == 1:
                date_obj = timezone.make_aware(
                    timezone.datetime.combine(
                        incumbent_elections_q[0].date,
                        timezone.datetime.min.time(),
                    )
                )
            else:
                raise Exception(
                    "Could not match or find date for %s." % election_name
                )
            # Now that we have a date, get or create the Election
            try:
                ocd_elec = Election.objects.get(start_time=date_obj)
            except Election.DoesNotExist:
                ocd_elec = self.create_election(
                    '{year} {type}'.format(**parsed_name),
                    date_obj,
                )
                created = True
            else:
                created = False

        return (ocd_elec, created)

    def get_or_create_candidate_contest(self, office_name, ocd_election):
        """
        Get or create an OCD CandidateContest object using an office name and Election object.

        Returns a tuple (CandidateContest object, created), where created is a boolean
        specifying whether a CandidateContest was created.
        """
        post, post_created = self.get_or_create_post(office_name)

        q = post.contests.filter(contest__election=ocd_election)

        if post_created or not q.exists():
            contest = CandidateContest.objects.create(
                election=ocd_election,
                name=office_name,
                division=post.division,
            )
            contest.posts.create(
                post=post,
                contest=contest,
            )
            contest_created = True
        else:
            contest = q[0].contest
            contest_created = False

        return (contest, contest_created)

    def get_form501_filing(self, scraped_candidate):
        """
        Return a Form501Filing that matches the ScrapedCandidate.

        If the ScrapedCandidate has a scraped_id, lookup the Form501Filing
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
        q = Form501Filing.objects.filter(
            office__iexact=office_data['type'],
            district=office_data['district'],
            election_year=election_data['year'],
        )

        if scraped_candidate.scraped_id != '':
            try:
                form501 = q.get(filer_id=scraped_candidate.scraped_id)
            except Form501Filing.MultipleObjectsReturned:
                # if multiple form501s, try adding election type filter
                try:
                    form501 = q.get(
                        filer_id=scraped_candidate.scraped_id,
                        election_type=election_data['type'],
                    )
                except:
                    form501 = None
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
            try:
                form501 = q.get(
                    full_name=scraped_candidate.name,
                )
            except Form501Filing.MultipleObjectsReturned:
                # if multiple form501s, try adding election type filter
                try:
                    form501 = q.get(
                        full_name=scraped_candidate.name,
                        election_type=election_data['type'],
                    )
                except:
                    form501 = None
            except Form501Filing.DoesNotExist:
                # then try "<last_name>, <first_name> <middle_name>" format.
                q = q.annotate(
                    full_name=Concat(
                        'last_name',
                        Value(', '),
                        'first_name',
                        'middle_name',
                        output_field=CharField(),
                    ),
                )
                try:
                    form501 = q.get(
                        full_name=scraped_candidate.name,
                    )
                except Form501Filing.MultipleObjectsReturned:
                    # if multiple form501s, try adding election type filter
                    try:
                        form501 = q.get(
                            ffull_name=scraped_candidate.name,
                            election_type=election_data['type'],
                        )
                    except:
                        form501 = None
                except Form501Filing.DoesNotExist:
                    form501 = None

        return form501

    def load(self):
        """
        Load OCD Election, CandidateContest and related models with data scraped from CAL-ACCESS website.
        """
        for scraped_election in CandidateScrapedElection.objects.all():
            id_q = ElectionIdentifier.objects.filter(
                scheme='calaccess_election_id',
                identifier=scraped_election.scraped_id,
            )
            if id_q.exists():
                ocd_elec = id_q[0].election
            else:
                ocd_elec, elec_created = self.get_or_create_election_from_name(
                    scraped_election.name,
                )
                if elec_created and self.verbosity > 2:
                    self.log('Created new Election: %s' % ocd_elec.name)
                # Add the missing identifier
                ocd_elec.identifiers.create(
                    scheme='calaccess_election_id',
                    identifier=scraped_election.scraped_id,
                )
            # Whether Election is new or existing, update EventSource
            ocd_elec.sources.update_or_create(
                url=scraped_election.url,
                note='Last scraped on {dt:%Y-%m-%d}'.format(
                    dt=scraped_election.last_modified,
                )
            )
            # Loop over candidates of scraped election
            for scraped_candidate in scraped_election.candidates.all():
                contest, contest_created = self.get_or_create_candidate_contest(
                    scraped_candidate.office_name,
                    ocd_elec,
                )
                if (
                    'SPECIAL' in scraped_election.name and
                    not contest.previous_term_unexpired
                ):
                    contest.is_unexpired_term = True
                    contest.save()
                if contest_created and self.verbosity > 2:
                    self.log('Created new CandidateContest: %s' % contest.name)

                person, person_created = self.get_or_create_person(
                    scraped_candidate.name,
                    filer_id=scraped_candidate.scraped_id,
                )
                if person_created and self.verbosity > 2:
                    self.log('Created new Person: %s' % person.name)

                candidacy, candidacy_created = contest.candidacies.get_or_create(
                    person=person,
                    post=contest.posts.all()[0].post,
                    candidate_name=person.name,
                    registration_status='qualified',
                )
                if candidacy_created and self.verbosity > 2:
                    self.log('Created new Candidacy: %s' % candidacy)

                # try looking up form501 and supplementing scraped data
                form501 = self.get_form501_filing(scraped_candidate)
                if form501:
                    # try to lookup the party
                    try:
                        # first by full name
                        party = Party.objects.get(name=form501.party)
                    except Party.DoesNotExist:
                        try:
                            # then by abbrevation
                            party = Party.objects.get(abbreviation=form501.party)
                        except Party.DoesNotExist:
                            party = None

                    candidacy.extras = {'form501filingid': form501.filing_id}
                    candidacy.party = party
                    candidacy.filed_date = form501.date_filed
                    candidacy.save()

                    # if the scraped_candidate lacks a filer_id, add the
                    # Form501Filing.filer_id
                    if scraped_candidate.scraped_id == '':
                        candidacy.person.identifiers.get_or_create(
                            scheme='calaccess_filer_id',
                            identifier=form501.filer_id,
                        )

                # If the candidate has been in the post
                # and the end year is later than the election year
                # or doesn't have an end_date, mark as incumbent
                incumbent_q = Membership.objects.filter(
                    post=candidacy.post,
                    person=person,
                ).annotate(
                    # Cast end_date's value as an int, treat '' as NULL
                    end_year=Cast(
                        Case(When(end_date='', then=None)),
                        IntegerField(),
                    )
                ).filter(
                    Q(end_year__gt=contest.election.start_time.year) |
                    Q(end_date='')
                )
                if incumbent_q.exists():
                    candidacy.is_incumbent = True
                    candidacy.save()
                    self.log(' Identified as incumbent.')
        return
