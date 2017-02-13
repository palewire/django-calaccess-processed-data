#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing election information scraped from the CAL-ACCESS website.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.scraper.base import BaseScrapedElection


@python_2_unicode_compatible
class CandidateScrapedElection(BaseScrapedElection):
    """
    An election day scraped as part of the `scrapecalaccesscandidates` command.
    """
    scraped_id = models.CharField(
        verbose_name="election identification number",
        max_length=3,
        blank=True,
    )
    sort_index = models.IntegerField(
        null=True,
        help_text="The index value is used to preserve sorting of elections, "
                  "since multiple elections may occur in a year. A greater sort "
                  "index corresponds to a more recent election."
    )

    def __str__(self):
        return self.name
