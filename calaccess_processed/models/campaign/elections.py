#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing election data derived from scraped CAL-ACCESS data.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.managers import ProcessedDataManager


@python_2_unicode_compatible
class Election(models.Model):
    """
    California state elections.

    Derived from distinct year and type combinations in CandidateScrapedElection.
    """
    ELECTION_TYPE_CHOICES = (
        ('P', 'Primary'),
        ('G', 'General'),
        ('R', 'Recall'),
        ('SE', 'Special Election'),
        ('SR', 'Special Runoff'),
    )
    election_type = models.CharField(
        verbose_name="election type",
        max_length=2,
        choices=ELECTION_TYPE_CHOICES,
        help_text="Type of election",
    )
    OFFICE_CHOICES = (
        ('ASM', 'State Assembly'),
        ('GOV', 'Governor'),
        ('SEN', 'State Senate'),
    )
    office = models.CharField(
        verbose_name='office',
        null=True,
        max_length=3,
        choices=OFFICE_CHOICES,
        help_text='If a special election, office sought',
    )
    district = models.IntegerField(
        verbose_name='district',
        null=True,
        help_text='If a special election, district for the office sought (if '
                  'applicable)',
    )
    election_date = models.DateField(
        verbose_name="election date",
        help_text='Date of the election',
    )

    objects = ProcessedDataManager()

    def __str__(self):
        return '%s-%s' % (self.election_type, self.year)
