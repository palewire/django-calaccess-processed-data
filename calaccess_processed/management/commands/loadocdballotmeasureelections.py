#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load OCD Election models with data scraped from the CAL-ACCESS website.
"""
from calaccess_processed.models import OCDElectionProxy
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models import ScrapedPropositionElectionProxy


class Command(CalAccessCommand):
    """
    Load OCD Election models with data scraped from the CAL-ACCESS website.
    """
    help = 'Load OCD Election models with data scraped from the CAL-ACCESS website.'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.header("Load Ballot Measure Contests")

        # Loop over scraped elections for candidates
        for scraped_election in ScrapedPropositionElectionProxy.objects.all():

            # Get or create an election record
            ocd_election, ocd_created = self.get_or_create_ocd_election(scraped_election)

            # Whether Election is new or not, update EventSource
            ocd_election.sources.update_or_create(
                url=scraped_election.url,
                note='Last scraped on {:%Y-%m-%d}'.format(scraped_election.last_modified)
            )

        self.success("Done!")

    def get_or_create_ocd_election(self, scraped_election):
        """
        Get and OCD Election from scraped_election.
        """
        # Try getting an existing Election with the same date
        try:
            # Get the existing election
            return scraped_election.get_ocd_election(), False
        except OCDElectionProxy.DoesNotExist:
            # If we get this far, we are making a new election
            ocd_election = OCDElectionProxy.objects.create_from_calaccess(
                scraped_election.parsed_name,
                scraped_election.parsed_date,
            )

            # Log it out
            if self.verbosity > 1:
                self.log(' Created new Election: {}'.format(ocd_election))

            # Pass it back
            return ocd_election, True
