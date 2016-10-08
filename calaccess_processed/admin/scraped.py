#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for scraped models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.ScrapedElection)
class ScrapedElectionAdmin(BaseAdmin):
    list_display = (
        "election_id",
        "year",
        "date",
        "election_type",
    )
    list_filter = (
        "year",
        "election_type",
    )
    list_per_page = 500
    date_hierarchy = "date"
    search_fields = (
        "election_id",
        "year",
        "election_type",
    )


@admin.register(models.ScrapedCandidate)
class ScrapedCandidateAdmin(BaseAdmin):
    list_display = (
        "scraped_id",
        "name",
        "office_name",
        "office_seat",
        "election"
    )
    list_filter = (
        "election__year",
        "office_name",
    )
    list_per_page = 500
    search_fields = (
        "scraped_id",
        "name",
        "office_name",
        "office_seat"
    )


@admin.register(models.ScrapedProposition)
class ScrapedPropositionAdmin(BaseAdmin):
    list_display = (
        "scraped_id",
        "name",
        "election",
        "description"
    )
    list_filter = ("election__year",)
    list_per_page = 500
    search_fields = (
        "name",
        "description",
        "scraped_id"
    )
