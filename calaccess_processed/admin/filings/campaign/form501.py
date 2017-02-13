#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for campaign entity models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.Form501Filing)
class Form501FilingAdmin(BaseAdmin):
    """
    Custom admin for the Form501Filing model.
    """
    list_display = (
        'filing_id',
        'amendment_count',
        'date_filed',
        'committee_id',
        'last_name',
        'first_name',
        'office',
        'district',
        'party',
        'jurisdiction',
        'election_type',
        'election_year',
    )


@admin.register(models.Form501FilingVersion)
class Form501FilingVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form501FilingVersion model.
    """
    list_display = (
        'filing',
        'amend_id',
        'date_filed',
        'committee_id',
        'last_name',
        'first_name',
        'office',
        'district',
        'party',
        'jurisdiction',
        'election_type',
        'election_year',
    )
