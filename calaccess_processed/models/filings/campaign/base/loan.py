#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Abstract base models for campaign finance-related filings and transactions.
"""
from __future__ import unicode_literals
from django.db import models
from calaccess_processed.models.base import CalAccessBaseModel


class CampaignLoanItemBase(CalAccessBaseModel):
    """
    Abstract base model for loans received or made by campaign filers.

    These transactions are itemized on Schedules B (Parts 1 and 2) and H of
    Form 460 filings and stored in the LOAN_CD table.
    """
    line_item = models.IntegerField(
        verbose_name='line item',
        help_text="Line number of the filing form where the loan is "
                  "itemized (from LOAN_CD.LINE_ITEM)",
    )
    intermediary_title = models.CharField(
        verbose_name='intermediary title',
        max_length=10,
        blank=True,
        help_text='Name title of the intermediary (from LOAN_CD.INTR_NAMT)',
    )
    intermediary_lastname = models.CharField(
        verbose_name='intermediary lastname',
        max_length=200,
        blank=True,
        help_text='Last name of the intermediary or business name (from '
                  'LOAN_CD.INTR_NAML)',
    )
    intermediary_firstname = models.CharField(
        verbose_name='intermediary firstname',
        max_length=45,
        help_text='First name of the intermediary (from LOAN_CD.INTR_NAMF)',
    )
    intermediary_name_suffix = models.CharField(
        verbose_name='intermediary name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the intermediary (from LOAN_CD.INTR_NAMS)',
    )
    intermediary_city = models.CharField(
        verbose_name='intermediary city',
        max_length=30,
        blank=True,
        help_text='City of the intermediary (from LOAN_CD.INTR_CITY)',
    )
    intermediary_state = models.CharField(
        verbose_name='intermediary state',
        max_length=2,
        blank=True,
        help_text='State of the intermediary (from LOAN_CD.INTR_ST)',
    )
    intermediary_zip = models.CharField(
        verbose_name='intermediary zip',
        max_length=10,
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'intermediary (from LOAN_CD.INTR_ZIP4)',
    )
    interest_rate = models.CharField(
        verbose_name='interest rate',
        max_length=30,
        blank=True,
        help_text='Interest rate of the loan. This is sometimes expressed as a '
                  'decimal (e.g., 0.10) and other times as a percent (e.g., '
                  '10.0% (from LOAN_CD.LOAN_RATE)'
    )
    transaction_id = models.CharField(
        verbose_name='transaction id',
        max_length=20,
        help_text='Identifies a unique transaction across versions of the a '
                  'given Form 460 filing (from LOAN_CD.TRAN_ID)',
    )
    memo_reference_number = models.CharField(
        verbose_name='memo reference number',
        max_length=20,
        blank=True,
        help_text="A value assigned by the filer which refers to the item's"
                  "footnote in the TEXT_MEMO_CD table (from LOAN_CD."
                  "MEMO_REFNO)",
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


class CampaignLoanReceivedItemBase(CampaignLoanItemBase):
    """
    Abstract base model for loans received by campaign filers.

    These transactions are itemized on Schedule B (Parts 1 and 2) of Form 460
    filings and stored in the LOAN_CD table.
    """
    LENDER_CODE_CHOICES = (
        ('COM', "Committee"),
        ('IND', "Individual"),
        ('OTH', "Other"),
        ('PTY', "Political Party"),
        ('RCP', "Recipient committee"),
        ('SCC', "Small Contributor Committee"),
        ('???', "Unknown value"),
    )
    lender_code = models.CharField(
        verbose_name='lender code',
        max_length=3,
        blank=True,
        choices=LENDER_CODE_CHOICES,
        help_text='Code describing the lender (from LOAN_CD.ENTITY_CD)',
    )
    lender_committee_id = models.CharField(
        verbose_name='lender committee id',
        max_length=9,
        blank=True,
        help_text="lender's filer identification number, if it is a "
                  "committee (from LOAN_CD.CMTE_ID)",
    )
    lender_title = models.CharField(
        verbose_name='lender title',
        max_length=10,
        blank=True,
        help_text="Name title of the lender (from LOAN_CD.LNDR_NAMT)",
    )
    lender_lastname = models.CharField(
        verbose_name='lender lastname',
        max_length=200,
        blank=True,
        help_text="Last name of the lender or business name (from LOAN_CD."
                  "LNDR_NAML)",
    )
    lender_firstname = models.CharField(
        verbose_name='lender firstname',
        max_length=45,
        blank=True,
        help_text="First name of the lender (from LOAN_CD.LNDR_NAMF)",
    )
    lender_name_suffix = models.CharField(
        verbose_name='lender name suffix',
        max_length=10,
        blank=True,
        help_text="Name suffix of the lender (from LOAN_CD.LNDR_NAMS)",
    )
    lender_city = models.CharField(
        verbose_name='lender city',
        max_length=30,
        blank=True,
        help_text='City of the lender (from LOAN_CD.LOAN_CITY)',
    )
    lender_state = models.CharField(
        verbose_name='lender state',
        max_length=2,
        blank=True,
        help_text='State of the lender (from LOAN_CD.LOAN_ST)',
    )
    lender_zip = models.CharField(
        verbose_name='lender zip',
        max_length=10,
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'lender (from LOAN_CD.LOAN_ZIP4)',
    )
    lender_employer = models.CharField(
        verbose_name='lender employer',
        max_length=200,
        blank=True,
        help_text='Employer of the lender (from LOAN_CD.LOAN_EMP)',
    )
    lender_occupation = models.CharField(
        verbose_name='lender occupation',
        max_length=60,
        blank=True,
        help_text='Occupation of the lender (from LOAN_CD.LOAN_OCC)',
    )
    lender_is_self_employed = models.BooleanField(
        verbose_name='lender is self employed',
        default=False,
        help_text='Indicates whether or not the lender is self-employed'
                  '(from LOAN_CD.LOAN_SELF)',
    )
    treasurer_title = models.CharField(
        verbose_name='treasurer title',
        max_length=10,
        blank=True,
        help_text="Name title of the lender committee's treasurer (from "
                  "LOAN_CD.TRES_NAMT)",
    )
    treasurer_lastname = models.CharField(
        verbose_name='treasurer lastname',
        max_length=200,
        blank=True,
        help_text="Last name of the lender committee's treasurer (from "
                  "LOAN_CD.TRES_NAML)",
    )
    treasurer_firstname = models.CharField(
        verbose_name='treasurer firstname',
        max_length=45,
        help_text="First name of the lender committee's treasurer (from "
                  "LOAN_CD.TRES_NAMF)",
    )
    treasurer_name_suffix = models.CharField(
        verbose_name='treasurer name suffix',
        max_length=10,
        blank=True,
        help_text="Name suffix of the lender committee's treasurer (from "
                  "LOAN_CD.TRES_NAMS)",
    )
    treasurer_city = models.CharField(
        verbose_name='treasurer city',
        max_length=30,
        blank=True,
        help_text="City of the lender committee's treasurer (from LOAN_CD."
                  "TRES_CITY)",
    )
    treasurer_state = models.CharField(
        verbose_name='treasurer state',
        max_length=2,
        blank=True,
        help_text="State of the lender committee's treasurer (from LOAN_CD."
                  "TRES_ST)",
    )
    treasurer_zip = models.CharField(
        verbose_name='treasurer zip',
        max_length=10,
        blank=True,
        help_text="Zip code (usually zip5, sometimes zip9) of the lender "
                  "committee's treasurer (from LOAN_CD.TRES_ZIP4)",
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


class CampaignLoanMadeItemBase(CampaignLoanItemBase):
    """
    Abstract base model for loans made by campaign filers.

    These transactions are itemized on Schedule H of Form 460 filings and
    stored in the LOAN_CD table.
    """
    RECIPIENT_CODE_CHOICES = (
        ('COM', "Committee"),
        ('IND', "Individual"),
        ('OTH', "Other"),
        ('PTY', "Political Party"),
        ('RCP', "Recipient committee"),
        ('SCC', "Small Contributor Committee"),
        ('???', "Unknown value"),
    )
    recipient_code = models.CharField(
        verbose_name='recipient code',
        max_length=3,
        blank=True,
        choices=RECIPIENT_CODE_CHOICES,
        help_text='Code describing the recipient (from LOAN_CD.ENTITY_CD)',
    )
    recipient_committee_id = models.CharField(
        verbose_name='recipient committee id',
        max_length=9,
        blank=True,
        help_text="recipient's filer identification number, if it is a "
                  "committee (from LOAN_CD.CMTE_ID)",
    )
    recipient_title = models.CharField(
        verbose_name='recipient title',
        max_length=10,
        blank=True,
        help_text="Name title of the recipient (from LOAN_CD.LNDR_NAMT)",
    )
    recipient_lastname = models.CharField(
        verbose_name='recipient lastname',
        max_length=200,
        blank=True,
        help_text="Last name of the recipient or business name (from LOAN_CD."
                  "LNDR_NAML)",
    )
    recipient_firstname = models.CharField(
        verbose_name='recipient firstname',
        max_length=45,
        blank=True,
        help_text="First name of the recipient (from LOAN_CD.LNDR_NAMF)",
    )
    recipient_name_suffix = models.CharField(
        verbose_name='recipient name suffix',
        max_length=10,
        blank=True,
        help_text="Name suffix of the recipient (from LOAN_CD.LNDR_NAMS)",
    )
    recipient_city = models.CharField(
        verbose_name='recipient city',
        max_length=30,
        blank=True,
        help_text='City of the recipient (from LOAN_CD.LOAN_CITY)',
    )
    recipient_state = models.CharField(
        verbose_name='recipient state',
        max_length=2,
        blank=True,
        help_text='State of the recipient (from LOAN_CD.LOAN_ST)',
    )
    recipient_zip = models.CharField(
        verbose_name='recipient zip',
        max_length=10,
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'recipient (from LOAN_CD.LOAN_ZIP4)',
    )
    recipient_employer = models.CharField(
        verbose_name='recipient employer',
        max_length=200,
        blank=True,
        help_text='Employer of the recipient (from LOAN_CD.LOAN_EMP)',
    )
    recipient_occupation = models.CharField(
        verbose_name='recipient occupation',
        max_length=60,
        blank=True,
        help_text="Occupation of the recipient (from LOAN_CD.LOAN_OCC). Note "
                  "that, in some cases, the value seems to actually be the "
                  "recipient's committee ID.",
    )
    recipient_is_self_employed = models.BooleanField(
        verbose_name='recipient is self employed',
        default=False,
        help_text='Indicates whether or not the recipient is self-employed'
                  '(from LOAN_CD.LOAN_SELF)',
    )
    treasurer_title = models.CharField(
        verbose_name='treasurer title',
        max_length=10,
        blank=True,
        help_text="Name title of the recipient committee's treasurer (from "
                  "LOAN_CD.TRES_NAMT)",
    )
    treasurer_lastname = models.CharField(
        verbose_name='treasurer lastname',
        max_length=200,
        blank=True,
        help_text="Last name of the recipient committee's treasurer (from "
                  "LOAN_CD.TRES_NAML)",
    )
    treasurer_firstname = models.CharField(
        verbose_name='treasurer firstname',
        max_length=45,
        help_text="First name of the recipient committee's treasurer (from "
                  "LOAN_CD.TRES_NAMF)",
    )
    treasurer_name_suffix = models.CharField(
        verbose_name='treasurer name suffix',
        max_length=10,
        blank=True,
        help_text="Name suffix of the recipient committee's treasurer (from "
                  "LOAN_CD.TRES_NAMS)",
    )
    treasurer_city = models.CharField(
        verbose_name='treasurer city',
        max_length=30,
        blank=True,
        help_text="City of the recipient committee's treasurer (from LOAN_CD."
                  "TRES_CITY)",
    )
    treasurer_state = models.CharField(
        verbose_name='treasurer state',
        max_length=2,
        blank=True,
        help_text="State of the recipient committee's treasurer (from LOAN_CD."
                  "TRES_ST)",
    )
    treasurer_zip = models.CharField(
        verbose_name='treasurer zip',
        max_length=10,
        blank=True,
        help_text="Zip code (usually zip5, sometimes zip9) of the recipient "
                  "committee's treasurer (from LOAN_CD.TRES_ZIP4)",
    )

    class Meta:
        """
        Model options.
        """
        abstract = True
