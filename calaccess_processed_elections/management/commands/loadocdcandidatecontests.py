#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load the OCD CandidateContest and related models with scraped CAL-ACCESS data.
"""
from calaccess_processed_elections.proxies import (
    OCDCandidateContestProxy,
    OCDCandidacyProxy,
    ScrapedCandidateProxy
)
from calaccess_processed.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Load the OCD CandidateContest and related models with scraped CAL-ACCESS data.
    """
    help = 'Load the OCD CandidateContest and related models with scraped CAL-ACCESS data'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.header("Loading Candidate Contests")
        if self.verbosity > 2:
            self.log(" ...with CAL-ACCESS filer_ids")
            self.load_candidates_with_filer_ids()
        if self.verbosity > 2:
            self.log(" ...without CAL-ACCESS filer_ids")
            self.load_candidates_without_filer_ids()

        # connect runoffs to their previously undecided contests
        if self.verbosity > 2:
            self.log(' Linking runoffs to previous contests')
        OCDCandidateContestProxy.objects.set_parents()

        self.success("Done!")

    def load_candidates_with_filer_ids(self):
        """
        Load scraped candidates that were collected with a filer_id.
        """
        scraped_candidates = ScrapedCandidateProxy.objects.exclude(scraped_id='')

        for scraped_candidate in scraped_candidates:
            if self.verbosity > 2:
                self.log(f" Loading scraped candidate: {scraped_candidate}")
            candidacy = self.load_scraped_candidate(scraped_candidate)

            form501s = scraped_candidate.match_form501s_by_scraped_id()

            if form501s.exists():
                for form501 in form501s:
                    candidacy.link_form501(form501.filing_id)
                candidacy.update_from_form501()
                candidacy.link_filer_ids_from_form501s()

            self.correct_candidacy_party(scraped_candidate, candidacy)

    def load_candidates_without_filer_ids(self):
        """
        Load scraped candidates that were collected without a filer_id.

        These are the candidates on the state pages that are text only.

        They tend to be the least significant candidates, since they typically have never created a committee.
        """
        # Jim Fitzgerald's independent run for Senate 15 in 2008.
        # He was on the ballot in the general but records and a phone
        # interview with the candidate show he did not run in any primary.
        scraped_candidates = ScrapedCandidateProxy.objects.filter(
            scraped_id=''
        ).exclude(
            name__contains='FITZGERALD',
            election__name='2008 PRIMARY',
            office_name='STATE SENATE 15'
        )

        for scraped_candidate in scraped_candidates:
            if self.verbosity > 2:
                self.log(f" Loading scraped candidate: {scraped_candidate}")
            candidacy = self.load_scraped_candidate(scraped_candidate)

            form501s = scraped_candidate.match_form501s_by_name()

            if form501s.exists():
                for form501 in form501s:
                    candidacy.link_form501(form501.filing_id)
                candidacy.update_from_form501()
                candidacy.link_filer_ids_from_form501s()

            self.correct_candidacy_party(scraped_candidate, candidacy)

    def load_scraped_candidate(self, scraped_candidate):
        """
        Load a scraped_candidate into OCD Candidacy and related models.

        Returns a candidacy record.
        """
        # check if this scraped candidate was previously loaded into OCD
        try:
            candidacy = scraped_candidate.get_loaded_ocd_candidacy()
        except OCDCandidacyProxy.DoesNotExist:
            # Get contest
            contest, contest_created = scraped_candidate.get_or_create_contest()

            # Create candidacy
            candidacy, candidacy_created = OCDCandidacyProxy.objects.get_or_create_from_calaccess(
                contest,
                scraped_candidate.parsed_name,
                candidate_status='qualified',
                candidate_filer_id=scraped_candidate.scraped_id or None
            )
            if candidacy_created and self.verbosity > 1:
                self.log(' Created Candidacy: %s' % candidacy)
        else:
            # Get contest
            contest, contest_created = scraped_candidate.get_or_create_contest()
            # check if the candidacy is not part of the correct contest
            if contest != candidacy.contest:
                old_contest = candidacy.contest
                if self.verbosity > 2:
                    msg = ' Resetting {0} contest: {1} -> {2}'.format(
                        candidacy,
                        old_contest,
                        contest,
                    )
                    self.log(msg)
                candidacy.contest = contest
                candidacy.save()
                # if there aren't any candidacies linked to the old contest
                # delete it
                if old_contest.candidacies.count() == 0:
                    old_contest.delete()
                    if self.verbosity > 2:
                        self.log(' Deleting empty %s' % old_contest)

        # always update the source for the candidacy
        candidacy.sources.update_or_create(
            url=scraped_candidate.url,
            note='Last scraped on {dt:%Y-%m-%d}'.format(
                dt=scraped_candidate.last_modified,
            )
        )
        return candidacy

    def correct_candidacy_party(self, scraped_candidate, candidacy):
        """
        Correct the party of the candidacy, if necessary.
        """
        # Set candidacy party
        corrected_party = scraped_candidate.get_party()
        if corrected_party:
            # if not already set
            if not candidacy.party:
                candidacy.party = corrected_party
                candidacy.save()
            # or if correction is different
            elif candidacy.party.id != corrected_party.id:
                if self.verbosity > 2:
                    msg = ' Resetting {0} party: {1} -> {2}'.format(
                        candidacy,
                        candidacy.party,
                        corrected_party,
                    )
                    self.log(msg)
                candidacy.party = corrected_party
                candidacy.save()
