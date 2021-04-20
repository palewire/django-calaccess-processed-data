#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Managers for generating flatfiles that combine multiple table into a simplified file.
"""
from __future__ import unicode_literals
from django.db.models import F, Q, Max
from calaccess_processed.managers import BulkLoadSQLManager


class OCDFlatRetentionContestManager(BulkLoadSQLManager):
    """
    Custom manager for flattening contents of the OCD RetentionContest model.
    """
    def get_queryset(self):
        """
        Returns the custom QuerySet for this manager.
        """
        return super(
            OCDFlatRetentionContestManager, self
        ).get_queryset().filter(
            Q(identifiers__scheme='calaccess_measure_id')
            | Q(identifiers__isnull=True)
        ).annotate(
            office=F('membership__post__label'),
            office_holder=F('membership__person__name'),
            ocd_person_id=F('membership__person__id'),
            election_name=F('election__name'),
            election_date=F('election__date'),
            ocd_contest_id=F('id'),
            ocd_post_id=F('membership__post_id'),
            ocd_membership_id=F('membership_id'),
            ocd_election_id=F('election_id'),
            calaccess_measure_id=Max('identifiers__identifier')
        )
