#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load CandidateContest and related models with data scraped from the CAL-ACCESS website.
"""
from calaccess_processed.models import OCDRunoffProxy
from calaccess_processed.models import ScrapedCandidateProxy
from calaccess_processed.models import ScrapedCandidateElectionProxy
from calaccess_processed.management.commands import LoadOCDModelsCommand


class Command(LoadOCDModelsCommand):
    """
    Load CandidateContest and related models with data scraped from the CAL-ACCESS website.
    """
    help = 'Load CandidateContest and related models with data scraped from the CAL-ACCESS website.'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.header("Load Candidate Contests")

        # Load everything we can from the scrape
        self.load()

        # connect runoffs to their previously undecided contests
        if self.verbosity > 2:
            self.log(' Linking runoffs to previous contests')
        OCDRunoffProxy.objects.set_parents()

        self.success("Done!")

    def load(self):
        """
        Load OCD Election, CandidateContest and related models with data scraped from CAL-ACCESS website.
        """
        # Loop over scraped_elections
        for scraped_election in ScrapedCandidateElectionProxy.objects.all():

            # then over candidates in the scraped_election
            scraped_candidate_list = ScrapedCandidateProxy.objects.filter(election=scraped_election)
            for scraped_candidate in scraped_candidate_list:

                # Logging
                if self.verbosity > 2:
                    self.log(
                        ' Processing scraped Candidate.id {} ({})'.format(
                            scraped_candidate.id,
                            scraped_candidate
                        )
                    )

                #
                # Make a Candidacy
                #

                candidacy, candidacy_created = scraped_candidate.get_or_create_candidacy(
                    registration_status='qualified'
                )

                if candidacy_created and self.verbosity > 2:
                    msg = ' Created new Candidacy: {0.candidate_name} in {0.post.label}'.format(candidacy)
                    self.log(msg)

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

                # Fill the party if the candidacy doesn't have it
                # Get the candidate's party, looking in our correction file for any fixes
                if not candidacy.party:
                    party = scraped_candidate.get_party()
                    candidacy.party = party
                    candidacy.save()

                # always update the source for the candidacy
                candidacy.sources.update_or_create(
                    url=scraped_candidate.url,
                    note='Last scraped on {dt:%Y-%m-%d}'.format(
                        dt=scraped_candidate.last_modified,
                    )
                )
