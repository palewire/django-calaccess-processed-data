#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load CandidateContest and related models with data scraped from the CAL-ACCESS website.
"""
from django.db.models import IntegerField
from django.db.models import Case, When, Q
from django.db.models.functions import Cast
from opencivicdata.core.models import Membership
from calaccess_processed.models import OCDRunoffProxy
from calaccess_processed.models import ScrapedCandidateProxy
from calaccess_processed.models import ScrapedCandidateElectionProxy
from opencivicdata.elections.models import CandidateContest, Candidacy
from calaccess_processed.management.commands import LoadOCDModelsCommand


class Command(LoadOCDModelsCommand):
    """
    Load CandidateContest and related models with data scraped from the CAL-ACCESS website.
    """
    help = 'Load CandidateContest and related models with data scraped from the CAL-ACCESS website.'

    def add_arguments(self, parser):
        """
        Adds custom arguments specific to this command.
        """
        parser.add_argument(
            "--flush",
            action="store_true",
            dest="flush",
            default=False,
            help="Flush the database tables filled by this command."
        )

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.header("Load Candidate Contests")

        # Flush, if the options has been passed
        if options['flush']:
            self.flush()

        # Load everything we can from the scrape
        self.load()

        # connect runoffs to their previously undecided contests
        if self.verbosity > 2:
            self.log(' Linking runoffs to previous contests')
        OCDRunoffProxy.objects.set_parents()

        self.success("Done!")

    def flush(self):
        """
        Flush the database tables filled by this command.
        """
        models = [Candidacy, CandidateContest]
        for m in models:
            qs = m.objects.all()
            if self.verbosity > 0:
                self.log("Flushing {} {} objects".format(qs.count(), m.__name__))
            qs.delete()

    def load(self):
        """
        Load OCD Election, CandidateContest and related models with data scraped from CAL-ACCESS website.
        """
        # See if we should bother checking incumbent status
        members_are_loaded = Membership.objects.exists()

        # Loop over scraped_elections
        for scraped_election in ScrapedCandidateElectionProxy.objects.all():

            # Get election record
            ocd_election = scraped_election.get_ocd_election()

            # then over candidates in the scraped_election
            scraped_candidate_list = ScrapedCandidateProxy.objects.filter(election=scraped_election)
            for scraped_candidate in scraped_candidate_list:
                if self.verbosity > 2:
                    self.log(
                        ' Processing scraped Candidate.id {} ({})'.format(
                            scraped_candidate.id,
                            scraped_candidate
                        )
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

    def add_scraped_candidate_to_election(self, scraped_candidate, ocd_election):
        """
        Converts scraped_candidate from the CAL-ACCESS site to an OCD Candidacy. Links it to an ocd_election.

        Returns a candidacy object.
        """
        # Create contest
        contest, contest_created = scraped_candidate.get_or_create_contest()
        if contest_created and self.verbosity > 2:
            self.log(' Created new CandidateContest: {}'.format(contest.name))

        #
        # Get or create Candidacy
        #

        # Set default registration_status
        registration_status = 'qualified'

        # Correct any names we now are bad
        name_fixes = {
            # http://www.sos.ca.gov/elections/prior-elections/statewide-election-results/primary-election-march-7-2000/certified-list-candidates/ # noqa
            'COURTRIGHT DONNA': 'COURTRIGHT, DONNA'
        }
        scraped_candidate_name = name_fixes.get(
            scraped_candidate.name,
            scraped_candidate.name
        )

        candidacy, candidacy_created = self.get_or_create_candidacy(
            contest,
            scraped_candidate_name,
            registration_status,
            filer_id=scraped_candidate.scraped_id,
        )

        if candidacy_created and self.verbosity > 2:
            template = ' Created new Candidacy: {0.candidate_name} in {0.post.label}'
            self.log(template.format(candidacy))

        #
        # Dress it up with extra
        #

        # add extra data from form501, if available
        form501 = scraped_candidate.get_form501_filing()

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

        # Fill the party if the candidacy doesn't have it
        # Get the candidate's party, looking in our correction file for any fixes
        if not candidacy.party:
            party = scraped_candidate.get_party()
            if party:
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
