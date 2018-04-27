#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for campaign models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed_filings import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.Form461Filing)
class Form461FilingAdmin(BaseAdmin):
    """
    Custom admin for the Form461Filing model.
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


@admin.register(models.Form461FilingVersion)
class Form461FilingVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form461FilingVersion model.
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


@admin.register(models.Form461Part5Item)
class Form461Part5ItemAdmin(BaseAdmin):
    """
    Custom admin for the Form461Part5Item model.
    """
    list_display = (
        'filing',
        'line_item',
        'expense_date',
        'payee_code',
        'payee_lastname',
        'payee_firstname',
        'amount',
        'cumulative_ytd_amount',
        'transaction_id',
    )


@admin.register(models.Form461Part5ItemVersion)
class Form461Part5ItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form461Part5ItemVersion model.
    """
    list_display = (
        'filing_version',
        'line_item',
        'expense_date',
        'payee_code',
        'payee_lastname',
        'payee_firstname',
        'amount',
        'cumulative_ytd_amount',
        'transaction_id',
    )
