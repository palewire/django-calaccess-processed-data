#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load the OCD Membership model with data from the scraped Incumbent model.
"""
from django.db.models import IntegerField
from django.db.models.functions import Cast
from opencivicdata.core.models import Membership
from opencivicdata.elections.models import Candidacy, CandidateContest
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models import OCDMembershipProxy, ScrapedIncumbentProxy


class Command(CalAccessCommand):
    """
    Load the OCD Membership model with data from the scraped Incumbent model.
    """
    help = 'Load the OCD Membership model with data from the scraped Incumbent model'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.header("Loading Incumbent Office Holders")
        self.load()
        self.set_end_dates()
        if Candidacy.objects.exists():
            self.set_incumbent_candidacies()
        self.success("Done!")

    def load(self):
        """
        Load OCD Election, Membership and related models with data scraped from CAL-ACCESS website.
        """
        for incumbent in ScrapedIncumbentProxy.objects.all():
            membership, created = OCDMembershipProxy.objects.get_or_create_from_calaccess(
                incumbent
            )
            if created and self.verbosity > 2:
                self.log(' Created new Membership: %s' % membership)
            # Handle start_date on membershipbership
            if created or membership.start_date == '':
                membership.start_date = incumbent.session
                membership.save()
            else:
                # increment start year down
                start = int(membership.start_date)
                if start > incumbent.session:
                    membership.start_date = incumbent.session
                    membership.save()

    def set_end_dates(self):
        """
        Set the end_date for each Membership based on the start_date of each successor.
        """
        for member in Membership.objects.all():
            # Each member's end year should be the start year of their successor.
            # Successor is the member in the same post with the earliest
            # start year greater than the incumbent's start year
            if member.start_date == '':
                start_year = 0
            else:
                start_year = int(member.start_date)

            successor_q = Membership.objects.exclude(
                start_date='',
            ).annotate(
                start_year=Cast('start_date', IntegerField()),
            ).filter(
                start_year__gt=start_year,
                post=member.post,
            ).order_by('start_year')

            if successor_q.exists():
                member.end_date = int(successor_q[0].start_date)
                member.save()

    def set_incumbent_candidacies(self):
        """
        Set is_incumbent for candidacies within each member's start/end years.
        """
        # For every one of the member's candidacies for the office where
        # the election of the contest happens after the start year
        # but before the end year, if it exists, mark as incumbent
        for member in Membership.objects.all():
            candidacies_q = member.person.candidacies.filter(
                contest__election__date__year__gt=int(member.start_date),
                post=member.post,
            ).exclude(is_incumbent=True)
            # Handle blank member end_date values
            if member.end_date != '':
                member_end_year = int(member.end_date)
                candidacies_q = candidacies_q.filter(
                    contest__election__date__year__lte=member_end_year
                )

            if candidacies_q.exists():
                rows = candidacies_q.update(is_incumbent=True)
                if self.verbosity > 2:
                    self.log(
                        ' {0} identified as incumbent in {1} contests'.format(
                            member.person.name,
                            rows,
                        )
                    )
        # loop over all contest with an incumbent candidate
        contests_q = CandidateContest.objects.filter(
            candidacies__is_incumbent=True
        )
        for contest in contests_q.all():
            # set is_incumbent False for all other candidacies in contest
            contest.candidacies.exclude(
                is_incumbent=True
            ).update(is_incumbent=False)

        return
