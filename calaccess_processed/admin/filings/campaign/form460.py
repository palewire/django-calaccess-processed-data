#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for campaign models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.Form460Filing)
class Form460FilingAdmin(BaseAdmin):
    """
    Custom admin for the Form460Filing model.
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


@admin.register(models.Form460FilingVersion)
class Form460FilingVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form460FilingVersion model.
    """
    list_display = (
        'filing',
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


@admin.register(models.Form460ScheduleASummary)
class Form460ScheduleASummaryAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleASummary model.
    """
    list_display = (
        'filing',
        'itemized_contributions',
        'unitemized_contributions',
        'total_contributions'
    )
    search_fields = (
        'filing__filing_id',
    )


@admin.register(models.Form460ScheduleASummaryVersion)
class Form460ScheduleASummaryVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleASummaryVersion model.
    """
    list_display = (
        'filing_version',
        'itemized_contributions',
        'unitemized_contributions',
        'total_contributions'
    )


@admin.register(models.Form460ScheduleAItem)
class Form460ScheduleAItemAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleAItem model.
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


@admin.register(models.Form460ScheduleAItemVersion)
class Form460ScheduleAItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleAItemVersion model.
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


@admin.register(models.Form460ScheduleB1Item)
class Form460ScheduleB1ItemAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleB1Item model.
    """
    list_display = (
        'filing',
        'line_item',
        'lender_code',
        'lender_lastname',
        'begin_period_balance',
        'amount_received',
        'amount_paid',
        'amount_forgiven',
        'end_period_balance',
        'date_due',
        'interest_paid',
        'interest_rate',
        'original_amount',
        'date_incurred',
        'cumulative_ytd_contributions',
        'transaction_id',
    )


@admin.register(models.Form460ScheduleB1ItemVersion)
class Form460ScheduleB1ItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleB1ItemVersion model.
    """
    list_display = (
        'filing_version',
        'line_item',
        'lender_code',
        'lender_lastname',
        'begin_period_balance',
        'amount_received',
        'amount_paid',
        'amount_forgiven',
        'end_period_balance',
        'date_due',
        'interest_paid',
        'interest_rate',
        'original_amount',
        'date_incurred',
        'cumulative_ytd_contributions',
        'transaction_id',
    )


@admin.register(models.Form460ScheduleB2Item)
class Form460ScheduleB2ItemAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleB2Item model.
    """
    list_display = (
        'filing',
        'line_item',
        'guarantor_code',
        'guarantor_lastname',
        'amount_guaranteed_this_period',
        'balance_outstanding_to_date',
        'cumulative_ytd_amount',
        'loan_date',
        'transaction_id',
    )


@admin.register(models.Form460ScheduleB2ItemVersion)
class Form460ScheduleB2ItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleB2ItemVersion model.
    """
    list_display = (
        'filing_version',
        'line_item',
        'guarantor_code',
        'guarantor_lastname',
        'amount_guaranteed_this_period',
        'balance_outstanding_to_date',
        'cumulative_ytd_amount',
        'loan_date',
        'transaction_id',
    )


@admin.register(models.Form460ScheduleB2ItemOld)
class Form460ScheduleB2ItemOldAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleB2ItemOld model.
    """
    list_display = (
        'filing',
        'line_item',
        'lender_code',
        'lender_lastname',
        'date_repaid_or_forgiven',
        'date_of_original_loan',
        'interest_rate',
        'repayment_type',
        'amount_repaid_or_forgiven',
        'outstanding_principle',
        'interest_paid',
        'transaction_id',
    )


@admin.register(models.Form460ScheduleB2ItemVersionOld)
class Form460ScheduleB2ItemVersionOldAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleB2ItemVersionOld model.
    """
    list_display = (
        'filing_version',
        'line_item',
        'lender_code',
        'lender_lastname',
        'date_repaid_or_forgiven',
        'date_of_original_loan',
        'interest_rate',
        'repayment_type',
        'amount_repaid_or_forgiven',
        'outstanding_principle',
        'interest_paid',
        'transaction_id',
    )


@admin.register(models.Form460ScheduleCSummary)
class Form460ScheduleCSummaryAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleCSummary model.
    """
    list_display = (
        'filing',
        'itemized_contributions',
        'unitemized_contributions',
        'total_contributions'
    )
    search_fields = (
        'filing__filing_id',
    )


@admin.register(models.Form460ScheduleCSummaryVersion)
class Form460ScheduleCSummaryVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleCSummaryVersion model.
    """
    list_display = (
        'filing_version',
        'itemized_contributions',
        'unitemized_contributions',
        'total_contributions'
    )


@admin.register(models.Form460ScheduleCItem)
class Form460ScheduleCItemAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleCItem model.
    """
    list_display = (
        'filing',
        'line_item',
        'date_received',
        'fair_market_value',
        'transaction_id',
        'contributor_code',
        'contributor_lastname',
        'contributor_firstname',
    )


@admin.register(models.Form460ScheduleCItemVersion)
class Form460ScheduleCItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleCItemVersion model.
    """
    list_display = (
        'filing_version',
        'line_item',
        'date_received',
        'fair_market_value',
        'transaction_id',
        'contributor_code',
        'contributor_lastname',
        'contributor_firstname',
    )


@admin.register(models.Form460ScheduleDItem)
class Form460ScheduleDItemAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleDItem model.
    """
    list_display = (
        'filing',
        'line_item',
        'expense_date',
        'payee_code',
        'payee_lastname',
        'payee_firstname',
        'support_oppose_code',
        'ballot_measure_name',
        'candidate_lastname',
        'amount',
        'cumulative_election_amount',
        'cumulative_ytd_amount',
        'transaction_id',
    )


@admin.register(models.Form460ScheduleDItemVersion)
class Form460ScheduleDItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleDItemVersion model.
    """
    list_display = (
        'filing_version',
        'line_item',
        'expense_date',
        'payee_code',
        'payee_lastname',
        'payee_firstname',
        'support_oppose_code',
        'ballot_measure_name',
        'candidate_lastname',
        'amount',
        'cumulative_election_amount',
        'cumulative_ytd_amount',
        'transaction_id',
    )


@admin.register(models.Form460ScheduleEItem)
class Form460ScheduleEItemAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleEItem model.
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


@admin.register(models.Form460ScheduleEItemVersion)
class Form460ScheduleEItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleEItemVersion model.
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


@admin.register(models.Form460ScheduleESubItem)
class Form460ScheduleESubItemAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleESubItem model.
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
        'parent_transaction_id',
        'memo_reference_number',
    )


@admin.register(models.Form460ScheduleESubItemVersion)
class Form460ScheduleESubItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleESubItemVersion model.
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
        'parent_transaction_id',
        'memo_reference_number',
    )


@admin.register(models.Form460ScheduleFItem)
class Form460ScheduleFItemAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleFItem model.
    """
    list_display = (
        'filing',
        'line_item',
        'payee_code',
        'payee_lastname',
        'payee_firstname',
        'begin_balance',
        'amount_paid',
        'amount_incurred',
        'end_balance',
        'transaction_id',
        'parent_transaction_id',
        'memo_reference_number',
    )


@admin.register(models.Form460ScheduleFItemVersion)
class Form460ScheduleFItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleFItemVersion model.
    """
    list_display = (
        'filing_version',
        'line_item',
        'payee_code',
        'payee_lastname',
        'payee_firstname',
        'begin_balance',
        'amount_paid',
        'amount_incurred',
        'end_balance',
        'transaction_id',
        'parent_transaction_id',
        'memo_reference_number',
    )


@admin.register(models.Form460ScheduleGItem)
class Form460ScheduleGItemAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleGItem model.
    """
    list_display = (
        'filing',
        'line_item',
        'agent_lastname',
        'agent_firstname',
        'expense_date',
        'payee_code',
        'payee_lastname',
        'payee_firstname',
        'amount',
        'cumulative_ytd_amount',
        'transaction_id',
        'parent_transaction_id',
        'parent_schedule',
        'memo_reference_number',
    )


@admin.register(models.Form460ScheduleGItemVersion)
class Form460ScheduleGItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleGItemVersion model.
    """
    list_display = (
        'filing_version',
        'line_item',
        'agent_lastname',
        'agent_firstname',
        'expense_date',
        'payee_code',
        'payee_lastname',
        'payee_firstname',
        'amount',
        'cumulative_ytd_amount',
        'transaction_id',
        'parent_transaction_id',
        'parent_schedule',
        'memo_reference_number',
    )


@admin.register(models.Form460ScheduleHItem)
class Form460ScheduleHItemAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleHItem model.
    """
    list_display = (
        'filing',
        'line_item',
        'recipient_code',
        'recipient_lastname',
        'begin_period_balance',
        'amount_loaned',
        'amount_paid',
        'amount_forgiven',
        'end_period_balance',
        'date_due',
        'interest_received',
        'interest_rate',
        'original_amount',
        'date_incurred',
        'cumulative_ytd_contributions',
        'transaction_id',
    )


@admin.register(models.Form460ScheduleHItemVersion)
class Form460ScheduleHItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleHItemVersion model.
    """
    list_display = (
        'filing_version',
        'line_item',
        'recipient_code',
        'recipient_lastname',
        'begin_period_balance',
        'amount_loaned',
        'amount_paid',
        'amount_forgiven',
        'end_period_balance',
        'date_due',
        'interest_received',
        'interest_rate',
        'original_amount',
        'date_incurred',
        'cumulative_ytd_contributions',
        'transaction_id',
    )


@admin.register(models.Form460ScheduleH2ItemOld)
class Form460ScheduleH2ItemOldAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleH2ItemOld model.
    """
    list_display = (
        'filing',
        'line_item',
        'recipient_code',
        'recipient_lastname',
        'date_repaid_or_forgiven',
        'date_of_original_loan',
        'interest_rate',
        'repayment_type',
        'amount_repaid_or_forgiven',
        'outstanding_principle',
        'transaction_id',
    )


@admin.register(models.Form460ScheduleH2ItemVersionOld)
class Form460ScheduleH2ItemVersionOldAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleH2ItemVersionOld model.
    """
    list_display = (
        'filing_version',
        'line_item',
        'recipient_code',
        'recipient_lastname',
        'date_repaid_or_forgiven',
        'date_of_original_loan',
        'interest_rate',
        'repayment_type',
        'amount_repaid_or_forgiven',
        'outstanding_principle',
        'transaction_id',
    )


@admin.register(models.Form460ScheduleIItem)
class Form460ScheduleIItemAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleIItem model.
    """
    list_display = (
        'filing',
        'line_item',
        'date_received',
        'amount',
        'receipt_description',
        'transaction_id',
        'contributor_code',
        'contributor_lastname',
        'contributor_firstname',
    )


@admin.register(models.Form460ScheduleIItemVersion)
class Form460ScheduleIItemVersionAdmin(BaseAdmin):
    """
    Custom admin for the Form460ScheduleIItemVersion model.
    """
    list_display = (
        'filing_version',
        'line_item',
        'date_received',
        'amount',
        'receipt_description',
        'transaction_id',
        'contributor_code',
        'contributor_lastname',
        'contributor_firstname',
    )
