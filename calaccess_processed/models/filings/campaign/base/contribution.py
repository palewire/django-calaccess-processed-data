#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Abstract base models for campaign finance-related filings and transactions.
"""
from __future__ import unicode_literals
from django.db import models
from calaccess_processed.models.base import CalAccessBaseModel


class CampaignContributionBase(CalAccessBaseModel):
    """
    Abstract base model for contributions received or made by campaign filers.

    These transactions are itemized on Schedules A, C and I of Form 460
    filings and stored in the RCPT_CD table.
    """
    line_item = models.IntegerField(
        verbose_name='line item',
        null=False,
        help_text='Line number of the filing form where the contribution is '
                  'itemized (from RCPT_CD.LINE_ITEM)',
    )
    date_received = models.DateField(
        verbose_name='date received',
        null=True,
        help_text='Date the contribution was received (from RCPT_CD.'
                  'RCPT_DATE)'
    )
    date_received_thru = models.DateField(
        verbose_name='date received thru',
        null=True,
        help_text='End date for late contributions received over a range of '
                  'days (from RCPT_CD.DATE_THRU)',
    )
    TRANSACTION_TYPE_CHOICES = (
        ('F', 'Forgiven Loan'),
        ('I', 'Intermediary'),
        ('R', 'Returned (Negative Amount?)'),
        ('T', 'Third Party Repayment'),
        ('X', 'Transfer'),
        ('', 'Unknown'),
        ('INC16168', 'INC16168'),
    )
    transaction_type = models.CharField(
        verbose_name='transaction type',
        max_length=255,
        choices=TRANSACTION_TYPE_CHOICES,
        help_text='Type of transaction (from RCPT_CD.TRAN_TYPE)',
    )
    transaction_id = models.CharField(
        verbose_name='transaction id',
        max_length=20,
        help_text='Identifies a unique transaction across versions of the a '
                  'given Form 460 filing (from RCPT_CD.TRAN_ID)'
    )
    memo_reference_number = models.CharField(
        verbose_name='memo reference number',
        max_length=20,
        blank=True,
        help_text='Reference number for the memo attached to the contribution '
                  '(from RCPT_CD.MEMO_REFNO)',
    )
    CONTRIBUTOR_CODE_CHOICES = (
        ('COM', 'Committee'),
        ('IND', 'Individual'),
        ('OFF', 'Officer'),
        ('OTH', 'Other'),
        ('PTY', 'Political Party'),
        ('RCP', 'Recipient committee'),
        ('SCC', 'Small Contributor Committee'),
    )
    contributor_code = models.CharField(
        verbose_name='contributor code',
        max_length=3,
        blank=True,
        choices=CONTRIBUTOR_CODE_CHOICES,
        help_text='Code describing the contributor (from RCPT_CD.ENTITY_CD)',
    )
    contributor_committee_id = models.CharField(
        verbose_name='contributor committee id',
        max_length=9,
        blank=True,
        help_text="Contributor's filer identification number, if it is a "
                  "committee (from RCPT_CD.CMTE_ID)",
    )
    contributor_title = models.CharField(
        verbose_name='contributor title',
        max_length=10,
        blank=True,
        help_text='Name title of the contributor (from RCPT_CD.CTRIB_NAMT)',
    )
    contributor_lastname = models.CharField(
        verbose_name='contributor lastname',
        max_length=200,
        blank=True,
        help_text='Last name of the contributor or business name (from '
                  'RCPT_CD.CTRIB_NAML)',
    )
    contributor_firstname = models.CharField(
        verbose_name='contributor firstname',
        max_length=45,
        help_text='First name of the contributor (from RCPT_CD.CTRIB_NAMF)',
    )
    contributor_name_suffix = models.CharField(
        verbose_name='contributor name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the contributor (from RCPT_CD.CTRIB_NAMS)',
    )
    contributor_city = models.CharField(
        verbose_name='contributor city',
        max_length=30,
        blank=True,
        help_text='City of the contributor (from RCPT_CD.CTRIB_CITY)',
    )
    contributor_state = models.CharField(
        verbose_name='contributor state',
        max_length=2,
        blank=True,
        help_text='State of the contributor (from RCPT_CD.CTRIB_ST)',
    )
    contributor_zip = models.CharField(
        verbose_name='contributor zip',
        max_length=10,
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'contributor (from RCPT_CD.CTRIB_ZIP4)',
    )
    contributor_employer = models.CharField(
        verbose_name='contributor employer',
        max_length=200,
        blank=True,
        help_text='Employer of the contributor (from RCPT_CD.CTRIB_EMP)',
    )
    contributor_occupation = models.CharField(
        verbose_name='contributor occupation',
        max_length=60,
        blank=True,
        help_text='Occupation of the contributor (from RCPT_CD.CTRIB_OCC)',
    )
    contributor_is_self_employed = models.BooleanField(
        verbose_name='contributor is self employed',
        default=False,
        help_text='Indicates whether or not the contributor is self-employed'
                  '(from RCPT_CD.CTRIB_SELF)',
    )
    intermediary_committee_id = models.CharField(
        verbose_name='intermediary committee id',
        blank=True,
        max_length=9,
        help_text="Intermediary's filer identification number, if it is a "
                  "committee (from RCPT_CD.INTR_CMTEID)",
    )
    intermediary_title = models.CharField(
        verbose_name='intermediary title',
        max_length=10,
        blank=True,
        help_text='Name title of the intermediary (from RCPT_CD.INTR_NAMT)',
    )
    intermediary_lastname = models.CharField(
        verbose_name='intermediary lastname',
        max_length=200,
        blank=True,
        help_text='Last name of the intermediary or business name (from '
                  'RCPT_CD.INTR_NAML)',
    )
    intermediary_firstname = models.CharField(
        verbose_name='intermediary firstname',
        max_length=45,
        help_text='First name of the intermediary (from RCPT_CD.INTR_NAMF)',
    )
    intermediary_name_suffix = models.CharField(
        verbose_name='intermediary name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the intermediary (from RCPT_CD.INTR_NAMS)',
    )
    intermediary_city = models.CharField(
        verbose_name='intermediary city',
        max_length=30,
        blank=True,
        help_text='City of the intermediary (from RCPT_CD.INTR_CITY)',
    )
    intermediary_state = models.CharField(
        verbose_name='intermediary state',
        max_length=2,
        blank=True,
        help_text='State of the intermediary (from RCPT_CD.INTR_ST)',
    )
    intermediary_zip = models.CharField(
        verbose_name='intermediary zip',
        max_length=10,
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'intermediary (from RCPT_CD.INTR_ZIP4)',
    )
    intermediary_employer = models.CharField(
        verbose_name='intermediary employer',
        max_length=200,
        blank=True,
        help_text='Employer of the intermediary (from RCPT_CD.INTR_EMP)',
    )
    intermediary_occupation = models.CharField(
        verbose_name='intermediary occupation',
        max_length=60,
        blank=True,
        help_text='Occupation of the intermediary (from RCPT_CD.INTR_OCC)',
    )
    intermediary_is_self_employed = models.BooleanField(
        verbose_name='intermediary is self employed',
        default=False,
        help_text='(from S497_CD.INTR_SELF)',
    )
    cumulative_ytd_amount = models.DecimalField(
        decimal_places=2,
        max_digits=14,
        null=True,
        help_text="Cumulative year-to-date amount given by the contributor "
                  "as of the given Form 460 filing (from RCPT_CD.CUM_YTD)",
    )
    cumulative_election_amount = models.DecimalField(
        decimal_places=2,
        max_digits=14,
        null=True,
        help_text="For filers subject to contribution limits, cumulative "
                  "amount given by the contributor during the election "
                  "cycle as of the given Form 460 filing (from RCPT_CD."
                  "CUM_OTH)"
    )

    class Meta:
        """
        Model options.
        """
        abstract = True
