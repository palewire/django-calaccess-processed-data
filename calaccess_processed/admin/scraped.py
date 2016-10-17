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
        "name",
        "year",
        "election_id",
    )
    list_filter = ("year",)
    list_per_page = 500
    search_fields = (
        "election_id",
        "year",
        "name",
    )


@admin.register(models.ScrapedCandidate)
class ScrapedCandidateAdmin(BaseAdmin):
    list_display = (
        "scraped_id",
        "name",
        "office_name",
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


@admin.register(models.ScrapedCommittee)
class ScrapedCommitteeAdmin(BaseAdmin):
    list_display = (
        "scraped_id",
        "name",
        "proposition",
        "position",
    )
    list_filter = ("proposition__election__year", "position")
    list_per_page = 500
    search_fields = (
        "scraped_id",
        "name",
    )
