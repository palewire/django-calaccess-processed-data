#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load OCD RetentionContest and related models with data scraped from CAL-ACCESS.
"""
import re
from opencivicdata.core.models import Membership
from opencivicdata.elections.models import RetentionContest
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed_elections.proxies import (
    OCDPostProxy,
    OCDPersonProxy,
    ScrapedCandidateProxy,
    ScrapedIncumbentProxy,
    ScrapedPropositionProxy
)


class Command(CalAccessCommand):
    """
    Load OCD RetentionContest and related models with data scraped from CAL-ACCESS.
    """
    help = 'Load OCD RetentionContest and related models with data scraped from CAL-ACCESS'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.header('Loading Retention Contests')
        self.load()
        self.success("Done!")

    def create_contest(self, scraped_prop, ocd_elec):
        """
        Create an OCD RetentionContest object derived from a ScrapedProposition.

        Return a RetentionContest object.
        """
        if scraped_prop.name == '2003 RECALL QUESTION':
            # look up most recently scraped record for Gov. Gray Davis
            incumbent = ScrapedCandidateProxy.objects.filter(
                name='DAVIS, GRAY',
                office_name__contains='GOVERNOR',
            ).latest('created')
        else:
            # extract the office name from the prop name
            office = [p.strip().replace("DISTRICT ", "") for p in scraped_prop.name.split("-") if 'DISTRICT' in p][0]
            session = re.search(r'\d{4}', scraped_prop.election.name).group()
            try:
                # look up the most recent scraped incumbent in the office
                incumbent = ScrapedIncumbentProxy.objects.filter(
                    office_name__contains=office,
                    session__lt=session
                )[0]
            except IndexError:
                raise Exception("Unknown Incumbent in %s." % scraped_prop.name)

        # get or create person and post objects
        person = OCDPersonProxy.objects.get_or_create_from_calaccess(
            incumbent.parsed_name,
            candidate_filer_id=incumbent.scraped_id
        )[0]
        post = OCDPostProxy.objects.get_or_create_by_name(incumbent.office_name)[0]

        # get or create membership object
        membership = Membership.objects.get_or_create(
            person=person,
            post=post,
            role=post.role,
            organization=post.organization,
            person_name=person.name,
        )[0]

        # set the start_date and end_date for Governor Gray Davis
        if scraped_prop.name == '2003 RECALL QUESTION':
            membership.start_date = '1999'
            membership.end_date = '2003'
            membership.save()

        # create the retention contest
        return RetentionContest.objects.create(
            election=ocd_elec,
            division=post.division,
            name=scraped_prop.name,
            membership=membership,
        )

    def load(self):
        """
        Load OCD ballot measure-related models with data scraped from CAL-ACCESS website.
        """
        object_list = ScrapedPropositionProxy.objects.filter(name__icontains='RECALL')
        for scraped_prop in object_list:
            ocd_election = scraped_prop.election_proxy.get_ocd_election()
            try:
                # Try getting the contest using scraped_id
                ocd_contest = ocd_election.retentioncontests.get(
                    identifiers__scheme='calaccess_measure_id',
                    identifiers__identifier=scraped_prop.scraped_id,
                )
            except RetentionContest.DoesNotExist:
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
