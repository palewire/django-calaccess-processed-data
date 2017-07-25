#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load OCD BallotMeasureContest and related models with data scraped from the CAL-ACCESS website.
"""
import re
from opencivicdata.core.models import Membership
from calaccess_scraped.models import PropositionElection
from opencivicdata.elections.models import RetentionContest
from calaccess_processed.management.commands.loadocdballotmeasurecontests import Command
from calaccess_processed.models import OCDPostProxy, ScrapedCandidateProxy, ScrapedIncumbentProxy


class Command(Command):
    """
    Load OCD RetentionContest and related models with data scraped from the CAL-ACCESS website.
    """
    help = 'Load OCD RetentionContest and related models with data scraped from the CAL-ACCESS website.'
    header_log = 'Loading Retention Contests'

    def get_scraped_elecs(self):
        """
        Get the scraped elections with propositions to load.

        Return QuerySet.
        """
        return PropositionElection.objects.filter(propositions__name__icontains='RECALL')

    def get_scraped_props(self, scraped_elec):
        """
        Get the scraped propositions within the scraped election to load.

        Return QuerySet.
        """
        return scraped_elec.propositions.filter(name__icontains='RECALL')

    def create_contest(self, scraped_prop, ocd_elec):
        """
        Create an OCD RetentionContest object derived from a ScrapedProposition.

        Return a RetentionContest object.
        """
        if scraped_prop.name == '2003 RECALL QUESTION':
            # look up most recently scraped record for Gov. Gray Davis
            incumbent = ScrapedCandidateProxy.objects.filter(
                name='DAVIS, GRAY',
                office_name='GOVERNOR',
            ).latest('created')
        else:
            # extract the office name from the prop name
            office = scraped_prop.name.split(' - ')[2].replace('DISTRICT ', '')
            try:
                # look up the most recent scraped incumbent in the office
                incumbent = ScrapedIncumbentProxy.objects.filter(
                    office_name__contains=office,
                    session__lt=re.search('\d{4}', scraped_prop.election.name).group()
                )[0]
            except IndexError:
                raise Exception("Unknown Incumbent in %s." % scraped_prop.name)

        # get or create person and post objects
        person = incumbent.get_or_create_person(filer_id=incumbent.scraped_id)[0]
        post = OCDPostProxy.objects.get_or_create_by_name(incumbent.office_name)[0]

        # get or create membership object
        membership = Membership.objects.get_or_create(
            person=person,
            post=post,
            role=post.role,
            organization=post.organization,
            person_name=person.sort_name,
        )[0]

        # set the start_date and end_date for Governor Gray Davis
        if scraped_prop.name == '2003 RECALL QUESTION':
            membership.start_date = '1999'
            membership.end_date = '2003'
            membership.save()

        # create the retention contest
        ocd_contest = RetentionContest.objects.create(
            election=ocd_elec,
            division=post.division,
            name=scraped_prop.name,
            membership=membership,
        )

        return ocd_contest
