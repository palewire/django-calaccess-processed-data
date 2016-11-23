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
    A single election.

    Derived from CandidateScrapedElection and CommitteeScrapedElection.
    """

    ELECTION_TYPE_CHOICES = (
        ('P', 'Primary'),
        ('G', 'General'),
        ('S', 'Special'),
        ('R', 'Recall')
    )
    election_type = models.CharField(
        verbose_name="election type",
        max_length=1,
        null=False,
        blank=True,
        choices=ELECTION_TYPE_CHOICES,
        help_text="Type of election",
    )
    year = models.CharField(
        verbose_name="election year",
        max_length=4,
        null=False,
        blank=True,
        help_text="Election year",
    )

    objects = ProcessedDataManager()

    def __str__(self):
        return self.election_type
