#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base models for storing information scraped from the CAL-ACCESS website.
"""
from __future__ import unicode_literals
from django.db import models
from calaccess_processed.models import base


class BaseScrapedModel(base.CalAccessBaseModel):
    """
    Abstract base model from which all scraped models inherit.
    """
    url = models.URLField(max_length=2000, null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Model options.
        """
        abstract = True


class BaseScrapedElection(BaseScrapedModel):
    """
    An election day scraped from the California Secretary of State's site.

    This is an abstract base model that creates two tables, one for elections
    scraped as part of the candidates scraper, and one for elections scraped
    as part of the propositions scraper.
    """
    name = models.CharField(
        max_length=200
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


class BaseScrapedCommittee(BaseScrapedModel):
    """
    An committee scraped from the California Secretary of State's site.

    This is an abstract base model that creates two tables, one for committees
    scraped as part of the candidates scraper, and one for committees scraped
    as part of the propositions scraper.
    """
    name = models.CharField(
        verbose_name="committee name",
        max_length=500
    )
    scraped_id = models.CharField(
        verbose_name="committee identification number",
        max_length=7
    )

    class Meta:
        """
        Model options.
        """
        abstract = True
