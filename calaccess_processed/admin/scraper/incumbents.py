#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for scraped candidate models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.IncumbentScrapedElection)
class IncumbentScrapedElectionAdmin(BaseAdmin):
    """
    Custom admin for IncumbentScrapedElectionAdmin model.
    """
    list_display = (
        "name",
        "date",
    )
    list_per_page = 500
    search_fields = (
        "name",
    )


@admin.register(models.ScrapedIncumbent)
class ScrapedIncumbentAdmin(BaseAdmin):
    """
    Custom admin for ScrapedIncumbentAdmin model.
    """
    list_display = (
        "scraped_id",
        "name",
        "category",
        "office_name",
        "session",
    )
    list_filter = (
        "category",
        "office_name",
        "session",
    )
    list_per_page = 500
    search_fields = (
        "scraped_id",
        "name",
        "category",
        "office_name",
    )
