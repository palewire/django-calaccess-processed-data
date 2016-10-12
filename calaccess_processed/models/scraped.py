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
    name = models.CharField(
        verbose_name="scraped election name",
        max_length=200,
        null=False,
        blank=True,
        help_text="Scraped election name",
    )
    year = models.IntegerField(
        verbose_name='year of election',
        db_index=True,
        null=False,
        help_text='Year of election',
    )
    sort_index = models.IntegerField(
        verbose_name="sort index",
        null=False,
        help_text="The index value is used to preserve sorting of elections, \
        since multiple elections may occur in a year. A greater sort index \
        corresponds to a more recent election."
    )

    class Meta:
        ordering = ("-year",)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ScrapedCandidate(models.Model):
    name = models.CharField(
        verbose_name="candidate name",
        max_length=200,
        null=False,
        blank=False,
        help_text="Scraped candidate name",
    )
    scraped_id = models.CharField(
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
    election = models.ForeignKey(
        'ScrapedElection',
        null=True
    )

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ScrapedProposition(models.Model):
    # Most of the time, this is a number, however,
    # it can be a bona fide name, e.g.
    # '2003 Recall Question'
    name = models.CharField(
        verbose_name="proposition name",
        max_length=200,
        null=False,
        blank=False,
        help_text="Scraped proposition name",
    )
    description = models.TextField(
        verbose_name="proposition description",
        null=False,
        blank=True,
        help_text="Scraped proposition description",
    )
    scraped_id = models.CharField(
        verbose_name="proposition id",
        max_length=200,
        null=False,
        blank=False,
        help_text="Scraped proposition id",
    )
    election = models.ForeignKey(
        'ScrapedElection',
        null=True
    )

    class Meta:
        ordering = ("-election", "name")

    def __str__(self):
        return 'Proposition: {}'.format(self.name)


@python_2_unicode_compatible
class ScrapedCommittee(models.Model):
    name = models.CharField(
        verbose_name="committee name",
        max_length=500,
        null=False,
        blank=False,
        help_text="Scraped committee name",
    )
    scraped_id = models.CharField(
        verbose_name="committee id",
        max_length=7,
        null=False,
        blank=False,
        help_text="Scraped committee id",
    )
    support = models.BooleanField(
        verbose_name="supports proposition",
        help_text="Whether the committee supports the proposition",
    )
    proposition = models.ForeignKey(
        'ScrapedProposition',
        null=False
    )

    def __str__(self):
        return self.name
