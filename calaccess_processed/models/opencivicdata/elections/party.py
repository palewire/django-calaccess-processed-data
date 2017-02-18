#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OCD Election Party-related models.
"""
from __future__ import unicode_literals
from re import findall
from django.db import models
from calaccess_processed.models.opencivicdata.base import (
    LinkBase,
    OCDIDField,
    OCDBase,
)
from calaccess_raw.models.common import LookupCodesCd
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.base import CalAccessBaseModel


class PartyManager(models.Manager):
    """
    Manager with custom methods for OCD Party.
    """
    def load_raw_data(self):
        """
        Load Political Parties from raw LOOKUP_CODES_CD.
        """
        q = LookupCodesCd.objects.filter(
            code_type=16000,
            code_id__gt=16000,
        ).exclude(code_id__in=[16011, 16012])

        for lc in q:
            party = self.get_or_create(
                name=lc.code_desc,
                # combine the first char of each word (except AND) in party name
                abbreviation=''.join(
                    findall(
                        r'([A-z])\w+',
                        lc.code_desc.upper().replace(' AND ', '')
                    )
                ),
            )[0]
            if party.name in ['DEMOCRATIC', 'REPUBLICAN']:
                if party.name == 'DEMOCRATIC':
                    party.color = '1d0ee9'
                if party.name == 'REPUBLICAN':
                    party.color = 'e91d0e'
                party.save()
        return


@python_2_unicode_compatible
class Party(CalAccessBaseModel, OCDBase):
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

    class Meta:
        """
        Model options.
        """
        verbose_name_plural = 'parties'
        ordering = ("name",)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class PartySource(LinkBase):
    """
    Model for storing sources for OCD Party objects.
    """
    party = models.ForeignKey(Party, related_name='sources')

    def __str__(self):
        return self.url
