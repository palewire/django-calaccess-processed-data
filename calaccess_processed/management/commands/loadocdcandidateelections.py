#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load the OCD Election model with data from the ScrapedCandidateElection model.
"""
from datetime import date
from calaccess_processed.models import (
    ScrapedCandidateElectionProxy,
    OCDElectionProxy
)
from calaccess_processed.management.commands import CalAccessCommand
from opencivicdata.elections.models import Election


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
        self.header("Load Candidate Contests")
        self.load()
        self.success("Done!")

    def load(self):
        """
        Load OCD Election, CandidateContest and related models with data scraped from CAL-ACCESS website.
        """
        # Loop over scraped elections for candidates
        for scraped_election in ScrapedCandidateElectionProxy.objects.all():

            # Get or create an election record
            ocd_election, ocd_created = self.get_or_create_ocd_election(scraped_election)

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
            ocd_election = scraped_election.get_ocd_election()
        except Election.DoesNotExist:
            pass
        else:
            # If election does already exists and is named 'SPECIAL' or 'RECALL'...
            if ocd_election.is_special() or ocd_election.is_recall():
                # ... and the provided election_name includes either 'GENERAL' or 'PRIMARY'...
                if scraped_election.is_primary() or scraped_election.is_general():
                    # ... update the name
                    if self.verbosity > 2:
                        self.log(' Updated scraped name from {} to {}'.format(
                            ocd_election.name,
                            scraped_election.name
                        ))
                    ocd_election.name = scraped_election.name
                    ocd_election.extras['calaccess_election_type'] = scraped_election.parsed_name['type']
                    ocd_election.save()
            # If the match has a different scraped_id lets add that too
            ocd_election.identifiers.get_or_create(
                scheme='calaccess_election_id',
                identifier=scraped_election.scraped_id
            )
            # Then we're good to pass back the match
            return ocd_election, False

        # If we got this far, we are making a new election ...

        # Parse out data from the scraped object
        parsed_name = scraped_election.parsed_name
        parsed_date = scraped_election.parsed_date

        # Handle an edge case with bad data that conflates
        # the Feb 2008 Primary with the Jun 2008 Primary
        if scraped_election.name == '2008 PRIMARY':
            return OCDElectionProxy.objects.create_from_calaccess(
                scraped_election.name,
                date(2008, 6, 3),
                election_id=scraped_election.scraped_id,
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

        # Log it out
        if self.verbosity > 1:
            self.log(' Created new Election: {}'.format(ocd_election))

        # Finally pass it out.
        return ocd_election, True
