#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Campaign Disclosure Statements (Form 460).
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.filings.campaign import CampaignLoanMadeItemBase


class Form460ScheduleHItemBase(CampaignLoanMadeItemBase):
    """
    Abstract base model for items reported on Schedule H of Form 460.

    On Schedule H, campaign filers are required to report loans made or
    currently outstanding to other recipients during the period covered by the
    filing.
    """
    begin_period_balance = models.DecimalField(
        verbose_name='beginning period balance',
        decimal_places=2,
        max_digits=14,
        help_text="Outstanding balance of the loan at the beginning of the"
                  "period covered by the filing (from LOAN_CD.LOAN_AMT4)"
    )
    amount_loaned = models.DecimalField(
        verbose_name='amount loaned',
        decimal_places=2,
        max_digits=14,
        help_text="Amount loaned during the period covered by the filing "
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
        help_text="Amount forgiven by the campaign filer during the period "
                  "covered by the filing (from LOAN_CD.LOAN_AMT6)"
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
    interest_received = models.DecimalField(
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
                  "nonmonetary contributions) from the campaign filer to the "
                  "recipient during the calendar year covered by this statement"
                  " (from LOAN_CD.LOAN_AMT3)"
    )
    reported_on_h1 = models.BooleanField(
        verbose_name='reported on H1',
        default=False,
        help_text='Indicates if the item was actually reported on Part 1 of '
                  'Schedule H. Until 2001, campaign filers were required to '
                  'report loans made to others on Part 1 of Schedule H, '
                  'separate from repayments or forgiveness of those loans '
                  '(Schedule H, Part 2)'
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleHItem(Form460ScheduleHItemBase):
    """
    Loans made by campaign filers to other recipients.

    These transactions are itemized on Schedule H of the most recent version of
    each Form 460 filing. For loans itemized on any version of any Form 460
    filing, see Form460ScheduleHItemVersion.

    Derived from LOAN_CD records where FORM_TYPE is 'H' or 'H1'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_h_items',
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
        verbose_name = "Form 460 (Campaign Disclosure) Schedule H item"

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleHItemVersion(Form460ScheduleHItemBase):
    """
    Every version of each loan made by a campaign filer another recipient.

    For outstanding loans itemized on Schedule H of the most recent version of
    each Form 460 filing, see Form460ScheduleHItem.

    Derived from LOAN_CD records where FORM_TYPE is 'H' or 'H1'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_h_items',
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
        verbose_name = "Form 460 (Campaign Disclosure) Schedule H item version"

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


class Form460ScheduleH2ItemBaseOld(CampaignLoanMadeItemBase):
    """
    Abstract base model for Schedule H, Part 2, items from Form 460 circa 2001.

    Until Form 460 was modified in 2001, campaign filers were required to report
    repayments on and forgiveness of loans made to others on Part 2 of Schedule
    H.
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
        ('H2F', 'Forgiven'),
        ('H2R', 'Repay'),
        ('H2T', 'Third party payment'),
    )
    repayment_type = models.CharField(
        verbose_name='repayment type',
        max_length=3,
        choices=REPAYMENT_TYPE_CHOICES,
        help_text='Indicates whether the item is a loan repayment to the '
                  'campaign filer, a repayment by a third-party or a loan '
                  'forgiveness by the campaign filer (from LOAN_CD.LOAN_TYPE)',
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
        help_text="Outstanding balance of the loan at the end of the period "
                  "covered by the filing (from LOAN_CD.LOAN_AMT2)"
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleH2ItemOld(Form460ScheduleH2ItemBaseOld):
    """
    Repayments on loans/forgiven loans made by campaign filers circa 2001.

    These transactions are itemized on Schedule H, Part 2, of the most recent
    version to each Form 460 filing in the pre-2001 format. For loan repayments
    and forgiven loans on any version of any Form 460 filing in the pre-2001
    format, see Form460ScheduleH2ItemVersionOld.

    Derived from LOAN_CD records where FORM_TYPE is 'H2'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_h2_items_old',
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
        verbose_name = "Form 460 (Campaign Disclosure) Schedule H2 old item"

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleH2ItemVersionOld(Form460ScheduleH2ItemBaseOld):
    """
    Every version of each repayment/forgiveness of a loan by a campaign filer circa 2001.

    For loan repayments and forgiven loans on any version of any Form 460 filing
    in the pre-2001 format, see Form460ScheduleH2ItemOld.

    Derived from LOAN_CD records where FORM_TYPE is 'H2'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_h2_items_old',
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
        verbose_name = "Form 460 (Campaign Disclosure) Schedule H2 old item version"

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )
