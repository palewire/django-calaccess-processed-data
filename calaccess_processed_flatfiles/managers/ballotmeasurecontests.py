#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Managers for generating flatfiles that combine multiple table into a simplified file.
"""
from __future__ import unicode_literals
from django.db.models import Q, F, Max
from calaccess_processed.managers import BulkLoadSQLManager


class OCDFlatBallotMeasureContestManager(BulkLoadSQLManager):
    """
    Custom manager for flattening contents of the OCD BallotMeasureContest model.
    """
    def get_queryset(self):
        """
        Returns the custom QuerySet for this manager.
        """
        qs = super(
            OCDFlatBallotMeasureContestManager, self
        ).get_queryset()
        return qs.filter(
            Q(identifiers__scheme='calaccess_measure_id')
            | Q(identifiers__isnull=True)
        ).annotate(
            election_name=F('election__name'),
            election_date=F('election__date'),
            ocd_contest_id=F('id'),
            ocd_election_id=F('election_id'),
            calaccess_measure_id=Max('identifiers__identifier')
        )
