#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OCD Election-related models.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.opencivicdata.event import Event
from calaccess_processed.models.scraped import (
    # CandidateScrapedElection,
    PropositionScrapedElection,
)
import re
from datetime import datetime


class ElectionManager(models.Manager):
    """
    Manager with custom methods for OCD Division.
    """

    def create(self, start_time, name, **kwargs):
        """
        Custom create method for Election objects.
        """
        return super(
            ElectionManager,
            self,
        ).create(
            start_time=start_time,
            name=name,
            state='st06',
            all_day=True,
            classification='E',
            **kwargs
        )

    def load_raw_data(self):
        """
        Load Election model from CandidateScrapedElection and PropositionScrapedElection.
        """
        date_name_regex = r'^(?P<date>[A-Z]+\s\d{1,2},\s\d{4})\s(?P<name>.+)'

        for e in PropositionScrapedElection.objects.all():
            match = re.match(date_name_regex, e.name)
            dt_obj = datetime.strptime(
                match.groupdict()['date'],
                '%B %d, %Y',
            )
            self.create(
                start_time=dt_obj,
                name='{0} {1}'.format(
                    dt_obj.year,
                    match.groupdict()['name']
                    # TODO: Set adminstrative_org, external identifiers, source, etc.
                )
            )

        # TODO: loop over CandidateScrapedElection, update/create?

        return


@python_2_unicode_compatible
class Election(Event):
    """
    OCD Election model.
    """
    objects = ElectionManager()

    administrative_org = models.ForeignKey(
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
