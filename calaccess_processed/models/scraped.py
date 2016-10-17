#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing information scraped from the CAL-ACCESS website.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.managers import ProcessedDataManager


class BaseScrapedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class ScrapedElection(BaseScrapedModel):
    """
    An election day scraped from the California Secretary of State's site.
    """
    election_id = models.CharField(
        verbose_name="election identification number",
        max_length=3,
        blank=True,
    )
    name = models.CharField(
        max_length=200,
        blank=True,
    )
    type = models.CharField(
        max_length=200,
        blank=True,
    )
    year = models.IntegerField(
        verbose_name='year of election',
        db_index=True
    )
    date = models.DateField(
        verbose_name="date of election",
        null=True
    )
    sort_index = models.IntegerField(
        null=True,
        help_text="The index value is used to preserve sorting of elections, \
since multiple elections may occur in a year. A greater sort index \
corresponds to a more recent election."
    )

    class Meta:
        ordering = ("-year",)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ScrapedCandidate(BaseScrapedModel):
    """
    A candidate for office scraped from the California Secretary of State's site.
    """
    name = models.CharField(max_length=200)
    scraped_id = models.CharField(
        verbose_name="candidate identification number",
        max_length=7,
        blank=True,  # Some don't have IDs on the website
    )
    office_name = models.CharField(max_length=100, blank=True)
    election = models.ForeignKey('ScrapedElection', null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ScrapedProposition(BaseScrapedModel):
    """
    A yes or no ballot measure for voters scraped from the
    California Secretary of State's site.
    """
    # Most of the time, this is a number, however,
    # it can be a bona fide name, e.g.
    # '2003 Recall Question'
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    scraped_id = models.CharField(
        verbose_name="proposition identification number",
        max_length=200
    )
    election = models.ForeignKey('ScrapedElection', null=True)

    class Meta:
        ordering = ("-election", "name")

    def __str__(self):
        return 'Proposition: {}'.format(self.name)


@python_2_unicode_compatible
class ScrapedCommittee(BaseScrapedModel):
    """
    A committee supporting or opposing a proposition scraped from the
    California Secretary of State's site.
    """
    proposition = models.ForeignKey('ScrapedProposition')
    name = models.CharField(max_length=500)
    scraped_id = models.CharField(
        verbose_name="committee identification number",
        max_length=7
    )
    position = models.CharField(
        max_length=100,
        help_text="Whether the committee supports or opposes the proposition",
    )

    def __str__(self):
        return self.name
