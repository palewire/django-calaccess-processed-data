#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for campaign models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.Schedule497Filing)
class Schedule497FilingAdmin(BaseAdmin):
    """
    Custom admin for the Schedule497Filing model.
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


@admin.register(models.Schedule497FilingVersion)
class Schedule497FilingVersionAdmin(BaseAdmin):
    """
    Custom admin for the Schedule497FilingVersion model.
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


@admin.register(models.Schedule497Part1Item)
class Schedule497Part1ItemAdmin(BaseAdmin):
    """
    Custom admin for the Schedule497Part1Item model.
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


@admin.register(models.Schedule497Part1ItemVersion)
class Schedule497Part1ItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Schedule497Part1ItemVersion model.
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


@admin.register(models.Schedule497Part2Item)
class Schedule497Part2ItemAdmin(BaseAdmin):
    """
    Custom admin for the Schedule497Part2Item model.
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


@admin.register(models.Schedule497Part2ItemVersion)
class Schedule497Part2ItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Schedule497Part2ItemVersion model.
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
