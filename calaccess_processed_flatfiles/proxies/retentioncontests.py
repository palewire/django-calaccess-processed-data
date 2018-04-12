#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for generating flatfiles that combine multiple table into a simplified file.
"""
from __future__ import unicode_literals
from opencivicdata.elections.models import RetentionContest
from calaccess_processed.proxies import OCDProxyModelMixin
from calaccess_processed_flatfiles.managers import OCDFlatRetentionContestManager


class OCDFlatRetentionContestProxy(RetentionContest, OCDProxyModelMixin):
    """
    Every recall measure.
    """
    objects = OCDFlatRetentionContestManager()

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
        app_label = "calaccess_processed_flatfiles"
        proxy = True
        verbose_name_plural = 'recall measures'
