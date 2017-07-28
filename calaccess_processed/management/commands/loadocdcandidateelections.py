#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load the OCD Election model with data from the ScrapedCandidateElection model.
"""
from calaccess_processed.models import (
    ScrapedIncumbentElectionProxy,
    ScrapedCandidateElectionProxy,
)
from calaccess_processed.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Load the OCD Election model with data from the ScrapedCandidateElection model.
    """
    help = 'Load the OCD Election model with data from the ScrapedCandidateElection model'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.header("Loading Election from scraped incumbents")
        self.load_from_proxy(ScrapedIncumbentElectionProxy)
        self.header("Loading Election from scraped candidates")
        self.load_from_proxy(ScrapedCandidateElectionProxy)
        self.success("Done!")

    def load_from_proxy(self, proxy):
        """
        Load OCD Election from scraped proxy model.
        """
        for scraped_election in proxy.objects.all():
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
