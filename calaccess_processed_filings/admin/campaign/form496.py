#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Admins for Schedule 497, the late contribution report.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed_filings import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.Form496Filing)
class Form496FilingAdmin(BaseAdmin):
    """
    Custom admin for the Form496Filing model.
    """
    list_display = (
        'filing_id',
        'amendment_count',
        'filer_id',
        'filer_lastname',
        'filer_firstname',
        'date_filed',
        'election_date',
    )


@admin.register(models.Form496FilingVersion)
class Form496FilingVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form496FilingVersion model.
    """
    list_display = (
        'filing',
        'amend_id',
        'filer_id',
        'filer_lastname',
        'filer_firstname',
        'date_filed',
        'election_date',
    )
