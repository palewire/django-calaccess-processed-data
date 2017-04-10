#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing incumbent information scraped from the CAL-ACCESS website.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.scraper.base import (
    BaseScrapedModel,
    BaseScrapedElection,
)


@python_2_unicode_compatible
class ScrapedIncumbent(BaseScrapedModel):
    """
    An incumbent state official scraped from the California Secretary of State's site.
    """
    session = models.IntegerField(
        verbose_name="session start year",
    )
    category = models.CharField(
        verbose_name="office category",
        max_length=100,
    )
    office_name = models.CharField(
        verbose_name="name of the office",
        max_length=100,
    )
    name = models.CharField(
        verbose_name="name of the incumbent",
        max_length=200,
    )
    scraped_id = models.CharField(
        verbose_name="scraped identification number",
        max_length=7,
    )

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class IncumbentScrapedElection(BaseScrapedElection):
    """
    An election day scraped as part of the `scrapecalaccessincumbents` command.
    """
    session = models.IntegerField(
        verbose_name="session start year",
    )
    date = models.DateField(
        verbose_name="election date",
    )

    def __str__(self):
        return self.name
