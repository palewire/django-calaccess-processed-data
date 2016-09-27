#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing information scraped from the CAL-ACCESS website.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.managers import ProcessedDataManager

@python_2_unicode_compatible
class ScrapedElection(models.Model):
    election_id = models.CharField(
        verbose_name="election identification number",
        max_length=3,
        null=False,
        blank=True,
        help_text="Election identification number",
    )
    election_year = models.IntegerField(
        verbose_name='year of election',
        db_index=True,
        null=False,
        help_text='Year of election',
    )
    election_type = models.CharField(
        verbose_name="election type",
        max_length=100,
        null=False,
        blank=True,
        help_text="Election type",
    )
    sort_index = models.IntegerField(
        verbose_name="sort index",
        null=False,
        help_text="The index value is used to preserve sorting of elections, \
        since multiple elections may occur in a year. A greater sort index \
        corresponds to a more recent election."
    )

    def __str__(self):
        return '{} {}'.format(self.election_year, self.election_type)


@python_2_unicode_compatible
class ScrapedCandidate(models.Model):
    candidate_name = models.CharField(
        verbose_name="candidate name",
        max_length=200,
        null=False,
        blank=False,
        help_text="Scraped candidate name",
    )
    candidate_id = models.CharField(
        verbose_name="candidate id",
        max_length=7,
        null=False,
        # Some don't have IDs on the website
        blank=True,
        help_text="Scraped candidate id",
    )
    office_name = models.CharField(
        verbose_name="office name",
        max_length=100,
        null=False,
        blank=True,
        help_text="Office name",
    )
    # Preserve leading zeroes
    office_seat = models.CharField(
        verbose_name="office seat number",
        max_length=3,
        null=False,
        blank=True,
        help_text="Office seat number",
    )
    election = models.ForeignKey(
        'ScrapedElection',
        null=True
    )

    def __str__(self):
        return str(self.candidate_name)
