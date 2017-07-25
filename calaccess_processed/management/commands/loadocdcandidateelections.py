#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load OCD Election models with data scraped from the CAL-ACCESS website.
"""
from datetime import date
from opencivicdata.core.models import Organization
from calaccess_processed.models import ScrapedCandidateElectionProxy, OCDDivisionProxy, OCDOrganizationProxy
from calaccess_processed.management.commands import CalAccessCommand
from opencivicdata.elections.models import Election


class Command(CalAccessCommand):
    """
    Load OCD Election models with data scraped from the CAL-ACCESS website.
    """
    help = 'Load OCD Election models with data scraped from the CAL-ACCESS website.'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        # Start it up.
        super(Command, self).handle(*args, **options)
        self.header("Load Candidate Contests")

        # Load everything we can from the scrape
        self.load()

        # connect runoffs to their previously undecided contests
        self.success("Done!")

    def load(self):
        """
        Load OCD Election, CandidateContest and related models with data scraped from CAL-ACCESS website.
        """
        # Loop over scraped elections for candidates
        for scraped_election in ScrapedCandidateElectionProxy.objects.all():

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

    def get_or_create_ocd_election(self, scraped_election):
        """
        Get and OCD Election from scraped_election.
        """
        # try looking up the election using the scraped id
        try:
            return scraped_election.get_ocd_election(), False
        except Election.DoesNotExist:
            pass

        # Parse out data from the scraped object
        parsed_name = scraped_election.parsed_name
        parsed_date = scraped_election.parsed_date

        # Handle an edge case with bad data that conflates
        # the Feb 2008 Primary with the Jun 2008 Primary
        if scraped_election.name == '2008 PRIMARY':
            return self.create_election(
                scraped_election.name,
                date(2008, 6, 3),
                scraped_id=scraped_election.scraped_id,
                election_type="PRIMARY",
            ), True

        # If we can't parse out a date, we should just quit now
        if not parsed_date:
            raise Exception("Could not match or find date for %s." % scraped_election.name)

        # If we can, let's create an election
        ocd_election = OCDElectionProxy.objects.create_from_calaccess(
            '{year} {type}'.format(**parsed_name),
            parsed_date,
            election_id=scraped_election.scraped_id,
            election_type=parsed_name['type'],
        )

        # If election does already exists and is named 'SPECIAL' or 'RECALL'...
        if (
            'SPECIAL' in ocd_election.name.upper() or
            'RECALL' in ocd_election.name.upper()
        ):
            # ... and the provided election_name includes either 'GENERAL' or 'PRIMARY'...
            if scraped_election.is_primary() or scraped_election.is_general():
                # ... update the name.
                ocd_election.name = scraped_election.name
                ocd_election.save()

        # Finally pass it out.
        return ocd_election, True
