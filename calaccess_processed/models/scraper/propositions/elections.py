#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing election information scraped from the CAL-ACCESS website.
"""
from __future__ import unicode_literals
import re
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.scraper.base import BaseScrapedElection


@python_2_unicode_compatible
class PropositionScrapedElection(BaseScrapedElection):
    """
    An election day scraped as part of the `scrapecalaccesspropositions` command.
    """
    def __str__(self):
        return self.name
