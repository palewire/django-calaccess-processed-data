#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load incumbent candidate data scraped from the CAL-ACCESS website into OCD models.
"""
import re
from django.utils import timezone
from django.db.models import IntegerField
from django.db.models.functions import Cast
from calaccess_processed.management.commands import LoadOCDModelsCommand
from calaccess_processed.models.scraper import (
    IncumbentScrapedElection,
    ScrapedIncumbent,
)
from opencivicdata.models import Membership
from opencivicdata.models.elections import Election, Candidacy


class Command(LoadOCDModelsCommand):
    """
    Load incumbent candidate data scraped from the CAL-ACCESS website into OCD models.
    """
    help = 'Load incumbent candidate data scraped from the CAL-ACCESS website into OCD models'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.load()
        self.set_end_dates()
        if Candidacy.objects.exists():
            self.log('')
            self.set_incumbent_candidacies()
        self.success("Done!")

    def get_or_create_election(self, scraped_elec):
        """
        Get or create an OCD Election object using the IncumbentScrapedElection.

        Returns a tuple (Election object, created), where created is a boolean
        specifying whether a Election was created.
        """
        dt_obj = timezone.make_aware(
            timezone.datetime.combine(scraped_elec.date, timezone.datetime.min.time())
        )
        name = '{0} {1}'.format(dt_obj.year, scraped_elec.name)
        try:
            elec = Election.objects.get(start_time=dt_obj)
        except Election.DoesNotExist:
            # or make a new one
            elec = self.create_election(name, dt_obj)
            created = True
        else:
            created = False
            # if election already exists and is named 'SPECIAL' or 'RECALL'
            if 'SPECIAL' in elec.name.upper() or 'RECALL' in elec.name.upper():
                # and the matched election's name includes either 'GENERAL'
                # or 'PRIMARY'...
                if (
                    re.match(r'^\d{4} GENERAL$', scraped_elec.name) or
                    re.match(r'^\d{4} PRIMARY$', scraped_elec.name)
                ):
                    # update the name
                    elec.name = name
                    elec.save()
        return (elec, created)

    def load(self):
        """
        Load OCD Election, Membership and related models with data scraped from CAL-ACCESS website.
        """
        for scraped_elec in IncumbentScrapedElection.objects.all():
            ocd_elec = self.get_or_create_election(scraped_elec)[0]
            ocd_elec.sources.update_or_create(
                url=scraped_elec.url,
                note='Last scraped on {dt:%Y-%m-%d}'.format(
                    dt=scraped_elec.last_modified,
                )
            )

        for incumbent in ScrapedIncumbent.objects.all().order_by('-session'):
            # Get or create post
            post, post_created = self.get_or_create_post(
                incumbent.office_name,
            )
            if post_created and self.verbosity > 2:
                self.log('Created new Post: %s' % post.label)
            # Get or person
            person, person_created = self.get_or_create_person(
                incumbent.name,
                filer_id=incumbent.scraped_id,
            )
            if person_created and self.verbosity > 2:
                self.log('Created new Person: %s' % person.name)
            # Get or membership for post and person
            membership, membership_created = Membership.objects.get_or_create(
                person=person,
                post=post,
                role=post.role,
                organization=post.organization,
                person_name=person.sort_name,
            )
            if membership_created and self.verbosity > 2:
                self.log('Created new Membership: %s' % membership)
            # Handle start_date on membership
            if membership_created or membership.start_date == '':
                membership.start_date = incumbent.session
                membership.save()
            else:
                # increment start year down
                start = int(membership.start_date)
                if start > incumbent.session:
                    membership.start_date = incumbent.session
                    membership.save()

        return

    def set_end_dates(self):
        """
        Set the end_date for each Membership based on the start_date of each successor.
        """
        for member in Membership.objects.all():
            # Each member's end year should be the start year of their successor.
            # Successor is the member in the same post with the earliest
            # start year greater than the incumbent's start year
            successor_q = Membership.objects.exclude(
                start_date='',
            ).annotate(
                start_year=Cast('start_date', IntegerField()),
            ).filter(
                start_year__gt=int(member.start_date),
                post=member.post,
            ).order_by('start_year')

            if successor_q.exists():
                member.end_date = int(successor_q[0].start_date)
                member.save()
        return

    def set_incumbent_candidacies(self):
        """
        Set is_incumbent for candidacies within each member's start/end years.
        """
        # For every one of the member's candidacies for the office where
        # the election of the contest happens after the start year
        # but before the end year, if it exists, mark as incumbent
        for member in Membership.objects.all():
            candidacies_q = member.person.candidacies.filter(
                contest__election__start_time__year__gt=int(member.start_date),
                post=member.post,
            ).exclude(is_incumbent=True)
            # Handle blank member end_date values
            if member.end_date != '':
                member_end_year = int(member.end_date)
                candidacies_q = candidacies_q.filter(contest__election__start_time__year__lte=member_end_year)

            if candidacies_q.exists():
                rows = candidacies_q.update(is_incumbent=True)
                self.log(
                    ' {0} identified as incumbent in {1} contests'.format(
                        member.person.name,
                        rows,
                    )
                )
        return
