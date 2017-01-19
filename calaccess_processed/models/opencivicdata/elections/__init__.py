#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OCD Election-related models.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.opencivicdata.base import OCDBase
from calaccess_processed.models.opencivicdata.event import Event


class ElectionsManager(models.Manager):
    """
    Manager with custom methods for OCD Division.
    """

    def create(self, start_time, state, kwargs):
        """
        Custom create method for Division objects.
        """
        return super(
            ElectionManager,
            self,
        ).create(
            start_time=start_time,
            name=name,
            state=state,
            all_day=True,
            classification='election',
            **kwargs
        )


@python_2_unicode_compatible
class Election(Event):
    """
    OCD Election model.
    """
    objects = ElectionsManager()

    administrative_org_id = models.ForeignKey(
        'Organization',
        related_name='elections',
        null=True,
        help_text='Reference to the OCD ``Organization`` that administers the election.',
    )
    state = models.CharField(
        max_length=4,
        help_text='FIPS code of the state where the election is being held. '
                  'Recorded in the format ``st{{fips}}`` to match references '
                  'to VIP elements.',
    )
    is_statewide = models.BooleanField(
        default=True,
        help_text='Indicates whether the election is statewide.',
    )

    def __str__(self):
        return self.name
