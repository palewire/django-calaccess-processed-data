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


@admin.register(models.Form496Part1Item)
class Form496Part1ItemAdmin(BaseAdmin):
    """
    Custom admin for the Form496Part1Item model.
    """
    list_display = (
        'filing',
        "candidate_title",
        "candidate_lastname",
        "candidate_firstname",
        "candidate_name_suffix",
        "candidate_office_code",
        "ballot_measure_name",
        "ballot_measure_number",
        "ballot_measure_jurisdiction",
        "support_opposition_code"
    )


@admin.register(models.Form496Part1ItemVersion)
class Form496Part1ItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form496Part1ItemVersion model.
    """
    list_display = (
        'filing_version',
        "candidate_title",
        "candidate_lastname",
        "candidate_firstname",
        "candidate_name_suffix",
        "candidate_office_code",
        "ballot_measure_name",
        "ballot_measure_number",
        "ballot_measure_jurisdiction",
        "support_opposition_code"
    )


@admin.register(models.Form496Part2Item)
class Form496Part2ItemAdmin(BaseAdmin):
    """
    Custom admin for the Form496Part2Item model.
    """
    list_display = (
        'filing',
        "line_item",
        "expense_date",
        "amount",
        "transaction_id",
    )


@admin.register(models.Form496Part2ItemVersion)
class Form496Part2ItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form496Part2ItemVersion model.
    """
    list_display = (
        'filing_version',
        "line_item",
        "expense_date",
        "amount",
        "transaction_id",
    )


@admin.register(models.Form496Part3Item)
class Form496Part3ItemAdmin(BaseAdmin):
    """
    Custom admin for the Form496Part3Item model.
    """
    list_display = (
        'filing',
        'line_item',
        'date_received',
        'amount',
        'transaction_id',
        'contributor_code',
        'contributor_lastname',
        'contributor_firstname',
    )


@admin.register(models.Form496Part3ItemVersion)
class Form496Part3ItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form496Part3ItemVersion model.
    """
    list_display = (
        'filing_version',
        'line_item',
        'date_received',
        'amount',
        'transaction_id',
        'contributor_code',
        'contributor_lastname',
        'contributor_firstname',
    )
