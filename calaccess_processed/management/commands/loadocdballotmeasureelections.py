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

            # Log it out
            if ocd_created and self.verbosity > 2:
                self.log(' Created new Election: {}'.format(ocd_election))

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
            ocd_election = scraped_election.get_ocd_election()
        except OCDElectionProxy.DoesNotExist:
            # or make a new one
            return OCDElectionProxy.objects.create_from_calaccess(
                scraped_election.parsed_name,
                scraped_election.parsed_date,
            ), True

        # Extra stuff after you've gotten a prexisting object to make sure it's up to date.
        created = False

        # # If election already exists and is named 'SPECIAL' or 'RECALL' ...
        # if ocd_election.is_special() or ocd_election.is_recall():
        #     # ... and the matched election's name includes either 'GENERAL' or 'PRIMARY'...
        #     if scraped_election.is_general() or scraped_election.is_primary():
        #         # Update the name, since it could change on the site
        #         ocd_election.name = scraped_election.parsed_name
        #         ocd_election.save()

        # Pass it back out
        return ocd_election, created
