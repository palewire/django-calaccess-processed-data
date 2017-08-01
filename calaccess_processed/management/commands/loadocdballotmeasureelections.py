#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load the OCD Election model from the scraped PropositionElection model.
"""
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models import ScrapedPropositionElectionProxy


class Command(CalAccessCommand):
    """
    Load the OCD Election model from the scraped PropositionElection model.
    """
    help = 'Load the OCD Election model from the scraped PropositionElection model'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.header("Loading Election from scraped propositions")

        # Loop over scraped elections for candidates
        for scraped_election in ScrapedPropositionElectionProxy.objects.all():

            # Get or create an election record
            ocd_election, ocd_created = scraped_election.get_or_create_ocd_election()

            # Log it out
            if self.verbosity > 1 and ocd_created:
                self.log(' Created new Election: {}'.format(ocd_election))

            # Whether Election is new or not, update EventSource
            ocd_election.sources.update_or_create(
                url=scraped_election.url,
                note='Last scraped on {:%Y-%m-%d}'.format(scraped_election.last_modified)
            )

        self.success("Done!")
