#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for campaign models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed import models
from calaccess_raw.admin.base import BaseAdmin

@admin.register(models.Candidate)
class CandidateAdmin(BaseAdmin):
    """
    Custom admin for the Candidate model.
    """
    list_display = (
        'filer_id',
        'last_name',
        'first_name',
        'middle_name',
        'name_suffix',
        'election_year',
        'f501_filing_id',
        'last_f501_amend_id',
        'office',
        'district',
        'agency',
        'party',
    )

@admin.register(models.CandidateCommittee)
class CandidateCommitteeAdmin(BaseAdmin):
    """
    Custom admin for the CandidateCommittee model.
    """
    list_display = (
        'candidate_filer_id',
        'committee_filer_id',
        'link_type_id',
        'link_type_description',
        'first_session',
        'last_session',
        'first_effective_date',
        'last_effective_date',
        'first_termination_date',
        'last_termination_date',
    )

@admin.register(models.F460Filing)
class F460FilingAdmin(BaseAdmin):
    """
    Custom admin for the F460Filing model.
    """
    list_display = (
        'filing_id',
        'amendment_count',
        'filer_id',
        'filer_lastname',
        'filer_firstname',
        'date_filed',
        'election_date',
        'total_contributions',
        'total_expenditures_made',
        'ending_cash_balance',
    )

@admin.register(models.F460FilingVersion)
class F460FilingVersionAdmin(BaseAdmin):
    """
    Custom admin for the F460FilingVersion model.
    """
    list_display = (
        'filing_id',
        'amend_id',
        'filer_id',
        'filer_lastname',
        'filer_firstname',
        'date_filed',
        'election_date',
        'total_contributions',
        'total_expenditures_made',
        'ending_cash_balance',
    )

@admin.register(models.S497Filing)
class S497FilingAdmin(BaseAdmin):
    """
    Custom admin for the S497Filing model.
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

@admin.register(models.S497FilingVersion)
class S497FilingVersionAdmin(BaseAdmin):
    """
    Custom admin for the S497FilingVersion model.
    """
    list_display = (
        'filing_id',
        'amend_id',
        'filer_id',
        'filer_lastname',
        'filer_firstname',
        'date_filed',
        'election_date',
    )

@admin.register(models.LateContributionReceived)
class LateContributionReceivedAdmin(BaseAdmin):
    """
    Custom admin for the LateContributionReceived model.
    """
    list_display = (
        'filing_id',
        'line_item',
        'date_received',
        'amount_received',
        'transaction_id',
        'contributor_code',
        'contributor_lastname',
        'contributor_firstname',
    )

@admin.register(models.LateContributionReceivedVersion)
class LateContributionReceivedVersionAdmin(BaseAdmin):
    """
    Custom admin for the LateContributionReceivedVersion model.
    """
    list_display = (
        'filing_id',
        'amend_id',
        'line_item',
        'date_received',
        'amount_received',
        'transaction_id',
        'contributor_code',
        'contributor_lastname',
        'contributor_firstname',
    )

@admin.register(models.LateContributionMade)
class LateContributionMadeAdmin(BaseAdmin):
    """
    Custom admin for the LateContributionMade model.
    """
    list_display = (
        'filing_id',
        'line_item',
        'date_received',
        'amount_received',
        'transaction_id',
        'recipient_code',
        'recipient_lastname',
        'recipient_firstname',
    )

@admin.register(models.LateContributionMadeVersion)
class LateContributionMadeVersionAdmin(BaseAdmin):
    """
    Custom admin for the LateContributionMadeVersion model.
    """
    list_display = (
        'filing_id',
        'amend_id',
        'line_item',
        'date_received',
        'amount_received',
        'transaction_id',
        'recipient_code',
        'recipient_lastname',
        'recipient_firstname',
    )
