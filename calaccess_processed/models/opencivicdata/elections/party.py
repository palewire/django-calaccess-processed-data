#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OCD Election Party-related models.
"""
from __future__ import unicode_literals
from re import findall
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.opencivicdata.base import (
    OCDIDField,
    OCDBase,
)
from calaccess_raw.models.common import LookupCodesCd


class PartyManager(models.Manager):
    """
    Manager with custom methods for OCD Party.
    """
    def load_raw_data(self):
        """
        Load Political Parties from raw LOOKUP_CODES_CD.
        """
        self.all().delete()

        q = LookupCodesCd.objects.filter(
            code_type=16000,
            code_id__gt=16001,
        ).exclude(code_id__in=[16011, 16012])

        for lc in q:
            self.create(
                name=lc.code_desc,
                # combine the first char of each word (except AND) in party name
                abbreviation=''.join(
                    findall(
                        r'([A-z])\w+',
                        lc.code_desc.upper().replace(' AND ', '')
                    )
                ),
            )

        return


@python_2_unicode_compatible
class Party(OCDBase):
    """
    Political party with which candidates may be affiliated.
    """
    objects = PartyManager()

    id = OCDIDField(
        ocd_type='party',
        help_text='Open Civic Data-style id in the format ``ocd-candidacy/{{uuid}}``.',
    )
    name = models.CharField(
        max_length=300,
        help_text='The name of the party.'
    )
    abbreviation = models.CharField(
        max_length=3,
        unique=True,
        help_text='An abbreviation for the party name.',
    )
    color = models.CharField(
        max_length=6,
        blank=True,
        help_text='Six-character hex code representing an HTML color string. '
                  'The pattern is ``[0-9a-f]{6}``.',
    )
    is_write_in = models.NullBooleanField(
        null=True,
        help_text='Indicates that the party is not officially recognized by a '
                  'local, state, or federal organization but, rather, is a '
                  '"write-in" in jurisdictions which allow candidates to free-'
                  'form enter their political affiliation.',
    )

    def __str__(self):
        return self.name
