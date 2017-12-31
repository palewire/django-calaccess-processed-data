#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for generating flatfiles that combine multiple table into a simplified file.
"""
from __future__ import unicode_literals
from ..proxies import OCDProxyModelMixin
from opencivicdata.elections.models import BallotMeasureContest
from postgres_copy import CopyQuerySet
from calaccess_processed.managers import OCDFlatBallotMeasureContestManager


class OCDFlatBallotMeasureContestProxy(BallotMeasureContest, OCDProxyModelMixin):
    """
    Every ballot measure.
    """
    objects = OCDFlatBallotMeasureContestManager.from_queryset(CopyQuerySet)()

    copy_to_fields = (
        ('name',
         'Name of the ballot measure, not necessarily as it appears on the ballot.'),
        ('classification',),
        ('election_name',
         'Name of the election in which the ballot measure is decided.'),
        ('election_date',
         'Date of the election in which the ballot measure is decided.'),
        ('description',),
        ('created_at',),
        ('updated_at',),
        ('ocd_contest_id',),
        ('ocd_election_id',
         BallotMeasureContest._meta.get_field('election').help_text),
        ('calaccess_measure_id',
         'Identifier assigned to the ballot measure by CAL-ACCESS.'),
    )

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
        verbose_name_plural = 'ballot measures'
