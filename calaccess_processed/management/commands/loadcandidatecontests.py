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
from calaccess_raw.models import FilerToFilerTypeCd
from opencivicdata.models import (
    Election,
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
            ('2001 SPECIAL RUNOFF (ASSEMBLY 65)', '2001-4-3'),
            ('2001 SPECIAL ELECTION (ASSEMBLY 65)', '2001-2-6'),
            ('2001 SPECIAL ELECTION (STATE SENATE 24)', '2001-3-26'),
        )

        if election_name in (x[0] for x in election_dates):
            date = dict(election_dates)[election_name]
            date_obj = timezone.make_aware(
                timezone.datetime.strptime(date, '%Y-%m-%d'),
            )
        else:
            # if not in the hard-coded list above, check the scraped
            # incumbent elections.
            parsed_name = self.parse_election_name(election_name)
            incumbent_elections_q = IncumbentScrapedElection.objects.filter(
                date__year=parsed_name['year'],
                name__icontains=parsed_name['type'],
            )
            if incumbent_elections_q.count() == 1:
                date_obj = timezone.make_aware(
                    timezone.datetime.combine(
                        incumbent_elections_q[0].date,
                        timezone.datetime.min.time(),
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

        # Avoid conflating the Feb 2008 Primary with the Jun 2008 Primary
        if election_name == '2008 PRIMARY':
            try:
                ocd_election = Election.objects.get(
                    name=election_name,
                    start_time=timezone.datetime(
                        2008, 6, 3, 0, 0, tzinfo=timezone.utc
                    ),
                )
            except Election.DoesNotExist:
                ocd_election = self.create_election(
                    election_name,
                    timezone.datetime(
                        2008, 6, 3, 0, 0, tzinfo=timezone.utc
                    ),
                )
                created = True
            else:
                created = False
        # See if we can use the name to look up the election date
        elif self.lookup_election_date_from_name(election_name):
            date_obj = self.lookup_election_date_from_name(election_name)
            # Now that we have a date, get or create the Election
            try:
                ocd_election = Election.objects.get(start_time=date_obj)
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
        Return a Form501Filing that matches the ScrapedCandidate.

        By default, return the latest Form501FilingVersion, unless earliest
        is set to True.

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

    def get_party_for_filer_id(self, filer_id, election_date):
        """
        Lookup the party for the given filer_id.

        Return None if not found.
        """
        try:
            party_cd = FilerToFilerTypeCd.objects.filter(
                filer_id=filer_id,
                effect_dt__lte=election_date,
            ).latest('effect_dt').party_cd
        except:
            party = None
        else:
            if party_cd != 0:
                party = Party.objects.get(identifiers__identifier=party_cd)
            else:
                party = None

        return party

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
                contest_name = '{0} ({1})'.format(office_name, party.name)
            else:
                contest_name = office_name

        contest, contest_created = CandidateContest.objects.get_or_create(
            election=ocd_election,
            name=contest_name,
            previous_term_unexpired=previous_term_unexpired,
            party=party,
            division=post.division
        )

        if contest_created:
            contest.posts.create(
                post=post,
            )

        return (contest, contest_created)

    def add_scraped_candidate_to_election(self, scraped_candidate, ocd_election):
        """
        Convert scraped_candidate to a Candidacy and add to ocd_election.

        Return a candidacy object.
        """
        # get the candidate's form501
        form501 = self.get_form501_filing(scraped_candidate)
        # and use it to get the candidate's party
        if form501:
            party = self.lookup_party(form501.party)
            if not party:
                party = self.get_party_for_filer_id(
                    int(form501.filer_id),
                    ocd_election.start_time.date(),
                )
        else:
            party = None

        # if it's a primary election before 2012, include party in
        # get_or_create_contest criteria (if we have a party)
        if (
            'PRIMARY' in scraped_candidate.election.name and
            ocd_election.start_time.year < 2012
        ):
            if not party:
                # use UNKNOWN party
                party = Party.objects.get(identifiers__identifier=16011)
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

        candidacy, candidacy_created = self.get_or_create_candidacy(
            contest,
            filer_id=scraped_candidate.scraped_id,
            person_name=scraped_candidate.name,
        )

        if candidacy_created and self.verbosity > 2:
            template = ' Created new Candidacy: {0.candidate_name} in {0.post.label}'
            self.log(template.format(candidacy))

        # add extra data from form501, if available
        if form501:
            candidacy.party = party
            candidacy.extras = {'form501filingid': form501.filing_id}
            # use the filed_date of the earliest version of the form501
            candidacy.filed_date = form501.versions.earliest('date_filed').date_filed
            candidacy.save()

            # if the scraped_candidate lacks a filer_id, add the
            # Form501Filing.filer_id
            if scraped_candidate.scraped_id == '':
                candidacy.person.identifiers.get_or_create(
                    scheme='calaccess_filer_id',
                    identifier=form501.filer_id,
                )

        return candidacy

    def check_incumbent_status(self, candidacy):
        """
        Check if the Candidacy is for the incumbent officeholder.

        Return True if:
        * Membership exists for the Person and Post linked to the Candidacy, and
        * Membership.end_date is NULL or has a year later year of Election.start_time
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
            Q(end_year__gt=candidacy.election.start_time.year) |
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
                election__start_time__lt=runoff_contest.election.start_time,
            ).latest(
                'election__start_time'
            )
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
        for scraped_election in CandidateScrapedElection.objects.all():
            ocd_election = self.get_ocd_election(scraped_election)
            # then over candidates in the scraped_election
            for scraped_candidate in scraped_election.candidates.all():
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

        return
