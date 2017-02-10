#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for scraped proposition models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.PropositionScrapedElection)
class PropositionScrapedElectionAdmin(BaseAdmin):
    """
    Custom admin for PropositionScrapedElectionAdmin model.
    """
    list_display = (
        "name",
    )
    list_per_page = 500
    search_fields = (
        "name",
    )


@admin.register(models.ScrapedProposition)
class ScrapedPropositionAdmin(BaseAdmin):
    """
    Custom admin for ScrapedPropositionAdmin model.
    """
    list_display = (
        "scraped_id",
        "name",
        "election",
    )
    list_per_page = 500
    search_fields = (
        "name",
        "scraped_id"
    )


@admin.register(models.ScrapedPropositionCommittee)
class ScrapedPropositionCommitteeAdmin(BaseAdmin):
    """
    Custom admin for ScrapedPropositionCommitteeAdmin model.
    """
    list_display = (
        "scraped_id",
        "name",
        "position",
        "proposition",
    )
    list_per_page = 500
    search_fields = (
        "scraped_id",
        "name",
        "position",
        "proposition",
    )
