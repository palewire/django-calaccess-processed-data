#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load OCD BallotMeasureContest and related models with data scraped from the CAL-ACCESS website.
"""
import re
from django.utils import timezone
from calaccess_processed.models import ScrapedPropositionElectionProxy, ScrapedPropositionProxy
from opencivicdata.elections.models import BallotMeasureContest
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models import OCDElectionProxy, OCDDivisionProxy


class Command(CalAccessCommand):
    """
    Load OCD BallotMeasureContest and related models with data scraped from the CAL-ACCESS website.
    """
    help = 'Load OCD BallotMeasureContest and related models with data scraped from the CAL-ACCESS website'
    header_log = 'Loading Ballot Measure Contests'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.header(self.header_log)
        self.load()
        self.success("Done!")

    def get_scraped_elecs(self):
        """
        Get the scraped elections with propositions to load.

        Return QuerySet.
        """
        return ScrapedPropositionElectionProxy.objects.all()

    def get_scraped_props(self, scraped_elec):
        """
        Get the scraped propositions within the scraped election to load.

        Return QuerySet.
        """
        # Recalls are being excluded so they can be loaded in a separate command.
        return ScrapedPropositionProxy.objects.filter(
            election=scraped_elec
        ).exclude(name__icontains='RECALL')

    def get_or_create_election(self, scraped_election):
        """
        Get or create an OCD Election object using the scraped PropositionElection.

        Returns a tuple (Election object, created), where created is a boolean
        specifying whether a Election was created.
        """
        # Try getting an existing Election with the same date
        try:
            ocd_election = OCDElectionProxy.objects.get(date=scraped_election.parsed_date)
        except OCDElectionProxy.DoesNotExist:
            # or make a new one
            ocd_election = OCDElectionProxy.objects.create_from_calaccess(
                scraped_election.parsed_name,
                scraped_election.parsed_date,
            )
            created = True
        else:
            created = False
            # If election already exists and is named 'SPECIAL' or 'RECALL' ...
            if ocd_election.is_special() or ocd_election.is_recall():
                # ... and the matched election's name includes either 'GENERAL' or 'PRIMARY'...
                if scraped_election.is_general() or scraped_election.is_primary():
                    # Update the name, since it could change on the site
                    ocd_election.name = scraped_election.parsed_name
                    ocd_election.save()
        # Pass it back out
        return ocd_election, created

    def create_contest(self, scraped_prop, ocd_elec):
        """
        Create an OCD BallotMeasureContest object derived from a ScrapedProposition.

        Return a BallotMeasureContest object.
        """
        # Create the object
        return BallotMeasureContest.objects.create(
            election=ocd_elec,
            division=OCDDivisionProxy.objects.california(),
            name=scraped_prop.name,
            classification=scraped_prop.classification,
        )

    def load(self):
        """
        Load OCD ballot measure-related models with data scraped from CAL-ACCESS website.
        """
        # Loop over scraped elections
        for scraped_elec in self.get_scraped_elecs():
            # Get or create an OCD election
            ocd_elec, elec_created = self.get_or_create_election(scraped_elec)
            if elec_created and self.verbosity > 2:
                self.log('Created new Election: %s' % ocd_elec.name)

            # Update or create the Election source
            ocd_elec.sources.update_or_create(
                url=scraped_elec.url,
                note='Last scraped on {dt:%Y-%m-%d}'.format(
                    dt=scraped_elec.last_modified,
                )
            )

            # Loop over election's scraped propositions
            for scraped_prop in self.get_scraped_props(scraped_elec):
                try:
                    # Try getting the contest using scraped_id
                    ocd_contest = ocd_elec.ballotmeasurecontests.get(
                        identifiers__scheme='calaccess_measure_id',
                        identifiers__identifier=scraped_prop.scraped_id,
                    )
                except BallotMeasureContest.DoesNotExist:
                    # If not there, create one
                    ocd_contest = self.create_contest(scraped_prop, ocd_elec)
                    # Add the options
                    ocd_contest.options.create(text='yes')
                    ocd_contest.options.create(text='no')
                    # Add the identifiers
                    ocd_contest.identifiers.create(
                        scheme='calaccess_measure_id',
                        identifier=scraped_prop.scraped_id,
                    )
                    if self.verbosity > 2:
                        self.log(
                            'Created new {0}: {1}'.format(
                                ocd_contest._meta.object_name,
                                ocd_contest,
                            )
                        )
                else:
                    # If the contest already exists, make sure the name is up-to-date
                    # because they could change on subsequent scrapes of the SoS website
                    if ocd_contest.name != scraped_prop.name:
                        ocd_contest.name = scraped_prop.name
                        ocd_contest.save()

                # Update or create the Contest source
                ocd_contest.sources.update_or_create(
                    url=scraped_prop.url,
                    note='Last scraped on {dt:%Y-%m-%d}'.format(
                        dt=scraped_prop.last_modified,
                    )
                )
