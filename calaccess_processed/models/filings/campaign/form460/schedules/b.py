#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Campaign Disclosure Statements (Form 460).
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.base import CalAccessBaseModel
from calaccess_processed.models.filings.campaign import CampaignLoanReceivedItemBase


class Form460ScheduleB1ItemBase(CampaignLoanReceivedItemBase):
    """
    Abstract base model for items reported on Schedule B, Part 1, of Form 460.

    On Schedule B, Part 1, campaign filers are required to report loans
    received or outstanding during the period covered by the filing.
    """
    begin_period_balance = models.DecimalField(
        verbose_name='beginning period balance',
        decimal_places=2,
        max_digits=14,
        help_text="Outstanding balance of the loan at the beginning of the"
                  "period covered by the filing (from LOAN_CD.LOAN_AMT4)"
    )
    amount_received = models.DecimalField(
        verbose_name='amount received',
        decimal_places=2,
        max_digits=14,
        help_text="Amount received during the period covered by the filing "
                  "(from LOAN_CD.LOAN_AMT1)"
    )
    amount_paid = models.DecimalField(
        verbose_name='amount paid',
        decimal_places=2,
        max_digits=14,
        help_text="Amount paid back during the period covered by the filing "
                  "(from LOAN_CD.LOAN_AMT5)"
    )
    amount_forgiven = models.DecimalField(
        verbose_name='amount forgiven',
        decimal_places=2,
        max_digits=14,
        help_text="Amount forgiven by the lender during the period covered by "
                  "the filing (from LOAN_CD.LOAN_AMT6)"
    )
    end_period_balance = models.DecimalField(
        verbose_name='end period balance',
        decimal_places=2,
        max_digits=14,
        help_text="Outstanding balance of the loan at the end of the period "
                  "covered by the filing (from LOAN_CD.LOAN_AMT2)"
    )
    date_due = models.DateField(
        verbose_name='date due',
        null=True,
        help_text="Date that the loan is due (from LOAN_CD.LOAN_DATE2)"
    )
    interest_paid = models.DecimalField(
        verbose_name='interest paid',
        decimal_places=2,
        max_digits=14,
        help_text="Amount of interest paid on the loan during the period "
                  "covered by the campaign filing (from LOAN_CD.LOAN_AMT7)"
    )
    original_amount = models.DecimalField(
        verbose_name='original amount',
        decimal_places=2,
        max_digits=14,
        help_text="Original amount loaned by the lender to the campaign filer "
                  "(from LOAN_CD.LOAN_AMT8)"
    )
    date_incurred = models.DateField(
        verbose_name='date incurred',
        null=True,
        help_text="Date the loan was made or received (from LOAN_CD.LOAN_DATE1)"
    )
    cumulative_ytd_contributions = models.DecimalField(
        verbose_name='cumulative year-to-date contributions',
        decimal_places=2,
        max_digits=14,
        help_text="Cumulative amount of contributions (loans, monetary and "
                  "nonmonetary contributions) received from the lender during "
                  "the calendar year covered by this statement (from LOAN_CD."
                  "LOAN_AMT3)"
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleB1Item(Form460ScheduleB1ItemBase):
    """
    Loans received and loan payments by campaign filers.

    These transactions are itemized on Schedule B, Part 1, of the most recent
    version of each Form 460 filing. For loans itemized on any version of any
    Form 460 filing, see Form460ScheduleB1ItemVersion.

    Derived from LOAN_CD records where FORM_TYPE is 'B1'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_b1_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the loan '
                  'was reported (from LOAN_CD.FILING_ID)',
    )

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing',
            'line_item',
        ),)
        verbose_name = "Form 460 (Campaign Disclosure) Schedule B item"

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleB1ItemVersion(Form460ScheduleB1ItemBase):
    """
    Every version of each loan received or loan payment made by a campaign filer.

    For outstanding loans itemized on Schedule B, Part 1, of the most recent
    version of each Form 460 filing, see Form460ScheduleB1Item.

    Derived from LOAN_CD records where FORM_TYPE is 'B1'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_b1_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the outstanding loan'
    )

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)
        verbose_name = "Form 460 (Campaign Disclosure) Schedule B item version"

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


class Form460ScheduleB2ItemBase(CalAccessBaseModel):
    """
    Abstract base model for items reported on Schedule B, Part 2, of Form 460.

    On Schedule B, Part 2, campaign filers are required to report loan
    guarantors, A "guarantor" is a third party that co-signs, endorses, or
    provides security for a loan, or establishes or provides security for a
    line of credit. A guarantor is also making a contribution.
    """
    line_item = models.IntegerField(
        verbose_name='line item',
        help_text="Line number of the filing form where the loan is "
                  "itemized (from LOAN_CD.LINE_ITEM)",
    )
    GUARANTOR_CODE_CHOICES = (
        ('COM', "Committee"),
        ('IND', "Individual"),
        ('OTH', "Other"),
        ('PTY', "Political Party"),
        ('SCC', "Small Contributor Committee"),
        ('???', "Unknown value"),
    )
    guarantor_code = models.CharField(
        verbose_name='lender code',
        max_length=3,
        blank=True,
        choices=GUARANTOR_CODE_CHOICES,
        help_text='Code describing the guarantor (from LOAN_CD.ENTITY_CD)',
    )
    guarantor_title = models.CharField(
        verbose_name='guarantor title',
        max_length=10,
        blank=True,
        help_text="Name title of the guarantor (from LOAN_CD.LNDR_NAMT)",
    )
    guarantor_lastname = models.CharField(
        verbose_name='guarantor lastname',
        max_length=200,
        blank=True,
        help_text="Last name of the guarantor or business name (from LOAN_CD."
                  "LNDR_NAML)",
    )
    guarantor_firstname = models.CharField(
        verbose_name='guarantor firstname',
        max_length=45,
        blank=True,
        help_text="First name of the guarantor (from LOAN_CD.LNDR_NAMF)",
    )
    guarantor_name_suffix = models.CharField(
        verbose_name='guarantor name suffix',
        max_length=10,
        blank=True,
        help_text="Name suffix of the guarantor (from LOAN_CD.LNDR_NAMS)",
    )
    guarantor_city = models.CharField(
        verbose_name='guarantor city',
        max_length=30,
        blank=True,
        help_text='City of the guarantor (from LOAN_CD.LOAN_CITY)',
    )
    guarantor_state = models.CharField(
        verbose_name='guarantor state',
        max_length=2,
        blank=True,
        help_text='State of the guarantor (from LOAN_CD.LOAN_ST)',
    )
    guarantor_zip = models.CharField(
        verbose_name='guarantor zip',
        max_length=10,
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'guarantor (from LOAN_CD.LOAN_ZIP4)',
    )
    guarantor_employer = models.CharField(
        verbose_name='guarantor employer',
        max_length=200,
        blank=True,
        help_text='Employer of the guarantor (from LOAN_CD.LOAN_EMP)',
    )
    guarantor_occupation = models.CharField(
        verbose_name='guarantor occupation',
        max_length=60,
        blank=True,
        help_text='Occupation of the guarantor (from LOAN_CD.LOAN_OCC)',
    )
    guarantor_is_self_employed = models.BooleanField(
        verbose_name='guarantor is self employed',
        default=False,
        help_text='Indicates whether or not the guarantor is self-employed'
                  '(from LOAN_CD.LOAN_SELF)',
    )
    lender_name = models.CharField(
        verbose_name='lender name',
        max_length=200,
        blank=True,
        help_text="Name of the lender (from LOAN_CD.INTR_NAML)"
    )
    amount_guaranteed_this_period = models.DecimalField(
        verbose_name='amount guaranteed this period',
        decimal_places=2,
        max_digits=14,
        help_text="Amount guaranteed for the period covered by the filing "
                  "(from LOAN_CD.LOAN_AMT1)"
    )
    balance_outstanding_to_date = models.DecimalField(
        verbose_name='balance outstanding to date',
        decimal_places=2,
        max_digits=14,
        help_text="Outstanding balance for which the guarantor is liable at "
                  "the close of the reporting period (from LOAN_CD.LOAN_AMT2)"
    )
    cumulative_ytd_amount = models.DecimalField(
        verbose_name='cumulative year-to-date amount',
        decimal_places=2,
        max_digits=14,
        help_text="Cumulative amount guaranteed during the calendar year "
                  "covered by the statement (from LOAN_CD.LOAN_AMT3)"
    )
    loan_date = models.DateField(
        verbose_name='loan date',
        null=True,
        help_text="Date of the loan or date the line of credit was established"
                  "(from LOAN_CD.LOAN_DATE1)"
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
    reported_on_b1 = models.BooleanField(
        verbose_name='reported on B1',
        default=False,
        help_text='Indicates if the item was actually reported on Part 1 of '
                  'Schedule B. Until 2001, campaign filers were required to '
                  'report guarantors of loans or lines of credit on Part 1 of '
                  'Schedule B.'
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleB2Item(Form460ScheduleB2ItemBase):
    """
    Guarantees of loans and lines of credit received by campaign filers.

    These transactions are itemized on Schedule B, Part 2, of the most recent
    version to each Form 460 filing. For guarantees itemized on
    any version of any Form 460 filing, see Form460ScheduleB2ItemVersion.

    Derived from LOAN_CD records where FORM_TYPE is 'B2'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_b2_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the loan '
                  'was reported (from LOAN_CD.FILING_ID)',
    )

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing',
            'line_item',
        ),)
        verbose_name = "Form 460 (Campaign Disclosure) Schedule B2 item"

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleB2ItemVersion(Form460ScheduleB2ItemBase):
    """
    Every version of each guarantee of a loan/line of credit to a campaign filer.

    For guaratees itemized on Schedule B, Part 1, of the most recent
    version of each Form 460 filing, see Form460ScheduleB2Item.

    Derived from LOAN_CD records where FORM_TYPE is 'B2'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_b2_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the outstanding loan',
    )

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)
        verbose_name = "Form 460 (Campaign Disclosure) Schedule B2 item version"

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


class Form460ScheduleB2ItemBaseOld(CampaignLoanReceivedItemBase):
    """
    Abstract base model for Schedule B, Part 2, items from Form 460 circa 2001.

    Until Form 460 was modified in 2001, campaign filers were required to report
    repayments made on loans received, loans forgiven, and loans repaid by a
    third party on Part 2 of Schedule B.
    """
    date_repaid_or_forgiven = models.DateField(
        verbose_name='date paid or forgiven',
        null=True,
        help_text="Date when the loan repayment or forgiveness occurred (from "
                  "LOAN_CD.LOAN_DATE2)"
    )
    date_of_original_loan = models.DateField(
        verbose_name='date of original loan',
        null=True,
        help_text="Date the loan was orginally made (from LOAN_CD.LOAN_DATE1)"
    )
    REPAYMENT_TYPE_CHOICES = (
        ('B2F', 'Forgiven'),
        ('B2R', 'Repay'),
        ('B2T', 'Third party payment'),
    )
    repayment_type = models.CharField(
        verbose_name='repayment type',
        max_length=3,
        choices=REPAYMENT_TYPE_CHOICES,
        help_text='Indicates whether the item is a loan repayment by the '
                  'campaign filer, a repayment by a third-party or a loan '
                  'forgiveness by the lender (from LOAN_CD.LOAN_TYPE)',
    )
    amount_repaid_or_forgiven = models.DecimalField(
        verbose_name='amount repaid or forgiven',
        decimal_places=2,
        max_digits=14,
        help_text="Amount paid back or forgiven during the period covered by "
                  "the filing (from LOAN_CD.LOAN_AMT1)"
    )
    outstanding_principle = models.DecimalField(
        verbose_name='outstanding principle',
        decimal_places=2,
        max_digits=14,
        help_text="Outstanding principle of the loan at the end of the period "
                  "covered by the filing (from LOAN_CD.LOAN_AMT2)"
    )
    interest_paid = models.DecimalField(
        verbose_name='interest paid',
        decimal_places=2,
        max_digits=14,
        help_text="Amount of interest paid on the loan during the period "
                  "covered by the campaign filing (from LOAN_CD.LOAN_AMT3)"
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleB2ItemOld(Form460ScheduleB2ItemBaseOld):
    """
    Repayments on loans/forgiven loans received by campaign filers circa 2001.

    These transactions are itemized on Schedule B, Part 2, of the most recent
    version to each Form 460 filing in the pre-2001 format. For loan repayments
    and forgiven loans on any version of any Form 460 filing in the pre-2001
    format, see Form460ScheduleB2ItemVersionOld.

    Derived from LOAN_CD records where LOAN_TYPE is not blank or LOAN_DATE1 is
    before December 22, 2000.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_b2_items_old',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the loan '
                  'transaction was reported (from LOAN_CD.FILING_ID)',
    )

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing',
            'line_item',
        ),)
        verbose_name = "Form 460 (Campaign Disclosure) Schedule B2 old item"

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleB2ItemVersionOld(Form460ScheduleB2ItemBaseOld):
    """
    Every version of each repayment/forgiveness of a loan to a campaign filer circa 2001.

    For loan repayments and forgiven loans on any version of any Form 460 filing
    in the pre-2001 format, see Form460ScheduleB2ItemOld.

    Derived from LOAN_CD records where LOAN_TYPE is not blank or LOAN_DATE1 is
    before December 22, 2000.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_b2_items_old',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the loan transaction'
    )

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)
        verbose_name = "Form 460 (Campaign Disclosure) Schedule B2 old item version"

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )
