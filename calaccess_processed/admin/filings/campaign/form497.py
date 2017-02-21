#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Admins for Schedule 497, the late contribution report.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.Form497Filing)
class Form497FilingAdmin(BaseAdmin):
    """
    Custom admin for the Form497Filing model.
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


@admin.register(models.Form497FilingVersion)
class Form497FilingVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form497FilingVersion model.
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


@admin.register(models.Form497Part1Item)
class Form497Part1ItemAdmin(BaseAdmin):
    """
    Custom admin for the Form497Part1Item model.
    """
    list_display = (
        'filing',
        'line_item',
        'date_received',
        'amount_received',
        'transaction_id',
        'contributor_code',
        'contributor_lastname',
        'contributor_firstname',
    )


@admin.register(models.Form497Part1ItemVersion)
class Form497Part1ItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form497Part1ItemVersion model.
    """
    list_display = (
        'filing_version',
        'line_item',
        'date_received',
        'amount_received',
        'transaction_id',
        'contributor_code',
        'contributor_lastname',
        'contributor_firstname',
    )


@admin.register(models.Form497Part2Item)
class Form497Part2ItemAdmin(BaseAdmin):
    """
    Custom admin for the Form497Part2Item model.
    """
    list_display = (
        'filing',
        'line_item',
        'date_received',
        'amount_received',
        'transaction_id',
        'recipient_code',
        'recipient_lastname',
        'recipient_firstname',
    )


@admin.register(models.Form497Part2ItemVersion)
class Form497Part2ItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form497Part2ItemVersion model.
    """
    list_display = (
        'filing_version',
        'line_item',
        'date_received',
        'amount_received',
        'transaction_id',
        'recipient_code',
        'recipient_lastname',
        'recipient_firstname',
    )
