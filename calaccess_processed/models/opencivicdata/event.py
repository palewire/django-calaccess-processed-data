#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OCD Event-related models.

Copied (with some modifications) from
https://github.com/opencivicdata/python-opencivicdata-django/blob/master/opencivicdata/models/event.py
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.opencivicdata.base import (
    OCDIDField,
    OCDBase,
)


@python_2_unicode_compatible
class Event(OCDBase):
    """
    OCD Event model.
    """
    id = OCDIDField(
        ocd_type='event',
        help_text='Open Civic Data-style id in the format ``ocd-event/{{uuid}}``',
    )
    name = models.CharField(
        max_length=300,
        help_text='Name of the event, examples include "Fiscal committee '
                  'meeting on April 10th” or “Appropriations - S/C on Article '
                  'II".',
    )
    description = models.TextField(
        blank=True,
        help_text='Description of the Event.',
    )
    CLASSIFICATION_CHOICES = (
        ('committee-meeting', 'Committee Meeting'),
        ('election', 'Election'),
        ('hearing', 'Hearing'),
    )
    classification = models.CharField(
        max_length=300,
        choices=CLASSIFICATION_CHOICES,
        help_text='Classification of the event.',
    )
    start_time = models.DateTimeField(
        help_text='Starting time of the event.',
    )
    timezone = models.CharField(
        max_length=300,
        help_text="Timezone in which the event's start_time and end_time is "
                  "expressed."
    )
    end_time = models.DateTimeField(
        null=True,
        help_text='Ending time of the event.',
    )
    all_day = models.BooleanField(
        default=False,
        help_text='Boolean value set to boolean ``True`` if the event is an '
                  'all-day event, otherwise it must be set to the boolean '
                  'value ``False``.',
    )

    def __str__(self):
        return self.name

    class Meta:
        """
        Model options.
        """
        index_together = [
            ['start_time', 'name']
        ]
