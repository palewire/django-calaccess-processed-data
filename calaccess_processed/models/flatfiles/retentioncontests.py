#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for generating flatfiles that combine multiple table into a simplified file.
"""
from __future__ import unicode_literals

# Models
from ..proxies import OCDProxyModelMixin
from opencivicdata.elections.models import RetentionContest

# Managers
from postgres_copy import CopyQuerySet
from calaccess_processed.managers import OCDFlatRetentionContestManager


class OCDFlatRetentionContestProxy(RetentionContest, OCDProxyModelMixin):
    """
    Every recall measure.
    """
    objects = OCDFlatRetentionContestManager.from_queryset(CopyQuerySet)()

    copy_to_fields = (
        ('name',),
        ('office_holder',
         'Name of the office holder.'),
        ('office',
         'Office held.'),
        ('election_name',
         'Name of the election in which the ballot measure is decided.'),
        ('election_date',
         'Date of the election in which the ballot measure is decided.'),
        ('description',),
        ('ocd_contest_id',),
        ('ocd_person_id',
         'Reference to the Person that is the office holder.'),
        ('ocd_post_id',
         'Reference to the Post that is the office.'),
        ('ocd_membership_id',
         RetentionContest._meta.get_field('membership').help_text),
        ('ocd_election_id',
         RetentionContest._meta.get_field('election').help_text),
        ('created_at',),
        ('updated_at',),
        ('calaccess_measure_id',
         'Identifier assigned to the ballot measure by CAL-ACCESS.'),
    )

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
        verbose_name_plural = 'recall measures'
