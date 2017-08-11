#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load the OCD CandidateContest and related models with scraped CAL-ACCESS data.
"""
import datetime
from calaccess_processed.models import (
    OCDCandidateContestProxy,
    OCDCandidacyProxy,
    ScrapedCandidateProxy,
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
        self.load()

        # connect runoffs to their previously undecided contests
        if self.verbosity > 2:
            self.log(' Linking runoffs to previous contests')
        OCDCandidateContestProxy.objects.set_parents()

        self.success("Done!")

    def load(self):
        """
        Loop over scraped Candidate objects and update or create OCD model objects.
        """
        # Load everything we can from the scrape
        for scraped_candidate in ScrapedCandidateProxy.objects.all():
            # Get contest
            contest, contest_created = scraped_candidate.get_or_create_contest()

            # check if this scraped candidate was previously loaded into OCD
            try:
                candidacy = scraped_candidate.get_loaded_ocd_candidacy()
            except OCDCandidacyProxy.DoesNotExist:
                # Create candidacy
                candidacy, candidacy_created = OCDCandidacyProxy.objects.get_or_create_from_calaccess(
                    contest,
                    scraped_candidate.parsed_name,
                    candidate_status='qualified',
                    candidate_filer_id=scraped_candidate.scraped_id or None
                )
                if candidacy_created and self.verbosity > 1:
                    msg = ' Created Candidacy: {0.candidate_name} in {0.post.label}'.format(candidacy)
                    self.log(msg)
            else:
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

            #
            # Blacklisted contests
            #

            # First, Jim Fitzgerald's independent run for Senate 15 in 2008.
            # He was on the ballot in the general but records and a phone
            # interview with the candidate show he did not run in any primary.
            if (
                contest.name == 'STATE SENATE 15 (NO PARTY PREFERENCE)' and
                contest.election.date == datetime.date(2008, 6, 3)
            ):
                if self.verbosity > 2:
                    self.log("Deleting blacklisted {}".format(contest))
                candidacy.delete()
                contest.delete()
                continue

            #
            # Dress it up with extra stuff
            #

            # add extra data from form501, if available
            form501 = scraped_candidate.get_form501_filing()

            if form501:
                candidacy.link_form501(form501)
                candidacy.update_from_form501(form501)

                # if the scraped_candidate lacks a filer_id, add the
                # Form501Filing.filer_id
                if scraped_candidate.scraped_id == '':
                    candidacy.person.identifiers.get_or_create(
                        scheme='calaccess_filer_id',
                        identifier=form501.filer_id,
                    )

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

            # always update the source for the candidacy
            candidacy.sources.update_or_create(
                url=scraped_candidate.url,
                note='Last scraped on {dt:%Y-%m-%d}'.format(
                    dt=scraped_candidate.last_modified,
                )
            )
