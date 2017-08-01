#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load OCD BallotMeasureContest and related models with scraped CAL-ACCESS data.
"""
from opencivicdata.elections.models import BallotMeasureContest
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models import ScrapedPropositionProxy, OCDDivisionProxy


class Command(CalAccessCommand):
    """
    Load OCD BallotMeasureContest and related models with scraped CAL-ACCESS data.
    """
    help = 'Load OCD BallotMeasureContest and related models with scraped CAL-ACCESS data'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.header('Loading Ballot Measure Contests')
        self.load()
        self.success("Done!")

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
        object_list = ScrapedPropositionProxy.objects.exclude(name__icontains='RECALL')
        for scraped_prop in object_list:
            ocd_election = scraped_prop.election_proxy.get_ocd_election()
            try:
                # Try getting the contest using scraped_id
                ocd_contest = ocd_election.ballotmeasurecontests.get(
                    identifiers__scheme='calaccess_measure_id',
                    identifiers__identifier=scraped_prop.scraped_id,
                )
            except BallotMeasureContest.DoesNotExist:
                # If not there, create one
                ocd_contest = self.create_contest(scraped_prop, ocd_election)
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
                        'Created {0}: {1}'.format(
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
