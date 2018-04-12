#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flush data from OCD models.
"""
from opencivicdata.core.models import (
    Jurisdiction,
    Membership,
    Organization,
    Person,
    Post
)
from opencivicdata.elections.models import (
    Candidacy,
    CandidateContest,
    Election,
    BallotMeasureContest,
    RetentionContest
)
from calaccess_processed.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Flush data from OCD models.
    """
    help = "Flush data from OCD models."

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        # Flush models
        qs_list = [
            Candidacy.objects.all(),
            CandidateContest.objects.all(),
            BallotMeasureContest.objects.all(),
            RetentionContest.objects.all(),
            Election.objects.all(),
            Membership.objects.all(),
            Person.objects.all(),
            Post.objects.all(),
            Organization.objects.all(),
            Jurisdiction.objects.all(),
        ]
        for qs in qs_list:
            if self.verbosity > 0:
                self.log("Flushing {} {} objects".format(qs.count(), qs.model.__name__))
            qs.delete()
