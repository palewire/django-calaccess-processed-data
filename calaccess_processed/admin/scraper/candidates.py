#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for scraped candidate models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.CandidateScrapedElection)
class CandidateScrapedElectionAdmin(BaseAdmin):
    """
    Custom admin for CandidateScrapedElectionAdmin model.
    """
    list_display = (
        "name",
    )
    list_per_page = 500
    search_fields = (
        "name",
    )


@admin.register(models.ScrapedCandidate)
class ScrapedCandidateAdmin(BaseAdmin):
    """
    Custom admin for ScrapedCandidateAdmin model.
    """
    list_display = (
        "scraped_id",
        "name",
        "office_name",
        "election"
    )
    list_filter = (
        "office_name",
    )
    list_per_page = 500
    search_fields = (
        "scraped_id",
        "name",
        "office_name",
    )


@admin.register(models.ScrapedCandidateCommittee)
class ScrapedCandidateCommitteeAdmin(BaseAdmin):
    """
    Custom admin for ScrapedCandidateCommitteeAdmin model.
    """
    list_display = (
        "scraped_id",
        "name",
        "candidate_id",
        "status",
    )
    list_per_page = 500
    search_fields = (
        "scraped_id",
        "name",
        "candidate_id",
        "status",
    )
