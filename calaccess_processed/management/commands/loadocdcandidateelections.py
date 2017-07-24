#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load OCD Election models with data scraped from the CAL-ACCESS website.
"""
from datetime import date
from opencivicdata.core.models import Organization
from calaccess_processed.models import ScrapedCandidateElectionProxy
from calaccess_processed.management.commands import LoadOCDModelsCommand
from opencivicdata.elections.models import Election, OCDDivisionProxy, OCDOrganizationProxy


class Command(LoadOCDModelsCommand):
    """
    Load OCD Election models with data scraped from the CAL-ACCESS website.
    """
    help = 'Load OCD Election models with data scraped from the CAL-ACCESS website.'

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
                scraped_election.scraped_id
            ), True

        # If we can't parse out a date, we should just quit now
        if not parsed_date:
            raise Exception("Could not match or find date for %s." % scraped_election.name)

        # If we can, let's create an election
        ocd_election = self.create_election(
            '{year} {type}'.format(**parsed_name),
            parsed_date,
            scraped_election.scraped_id
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

    def create_election(self, name, date, scraped_id=None):
        """
        Create an OCD Election object.
        """
        # Pull its parent division within OCD
        admin = Organization.objects.get_or_create(
            name='Elections Division',
            classification='executive',
            parent=OCDOrganizationProxy.objects.secretary_of_state(),
        )[0]

        # Create the election
        obj = Election.objects.create(
            date=date,
            name=name,
            administrative_organization=admin,
            division=OCDDivisionProxy.objects.california(),
        )

        # And add the identifier so we can find it in the future using scraped data
        if scraped_id:
            obj.identifiers.create(scheme='calaccess_election_id', identifier=scraped_id)

        # Pass it out.
        return obj
