#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Schedule 497, the Late Contribution Reports.

More about the filing: http://calaccess.californiacivicdata.org/documentation/calaccess-forms/f497/
"""
from __future__ import unicode_literals
from django.db import models
from calaccess_processed_filings.models.base import FilingBaseModel


class Form496ItemBase(FilingBaseModel):
    """
    Abstract base model for items reported on Schedule 496 filings.

    On Schedule 496, campaign filers report independent expenditures whose combined total is $1,000 or more
    to support or oppose a single candidate for office or a single ballot measure. Form 496 should be filed
    within 24-hours of making the expenditure during the 90 days immediately preceding the election.
    """
    line_item = models.IntegerField(
        verbose_name='line item',
        db_index=True,
        null=False,
        help_text='Line number of the filing form where the transaction is '
                  'itemized (from S497_CD.LINE_ITEM)',
    )
    date_received = models.DateField(
        verbose_name='date received',
        db_index=True,
        null=True,
        help_text='Date the late contribution was received (from S497_CD.'
                  'CTRIB_DATE, unless NULL then from S497_CD.DATE_THRU)'
    )
    date_received_thru = models.DateField(
        verbose_name='date received thru',
        null=True,
        help_text='End date for late contributions received over a range of '
                  'days(from S497_CD.DATE_THRU)',
    )
    amount_received = models.DecimalField(
        verbose_name='amount received',
        decimal_places=2,
        max_digits=16,
        help_text='Dollar amount received (from S497_CD.AMOUNT)',
    )
    transaction_id = models.CharField(
        verbose_name='transaction id',
        max_length=20,
        db_index=True,
        help_text='Identifies a unique transaction across versions of the a '
                  'given Schedule 497 filing (from S497_CD.TRAN_ID)'
    )
    memo_reference_number = models.CharField(
        verbose_name='memo reference number',
        max_length=20,
        blank=True,
        help_text='Reference number for the memo attached to the transaction '
                  '(from S497_CD.MEMO_REFNO)',
    )

    class Meta:
        """
        Model options.
        """
        app_label = 'calaccess_processed_filings'
        abstract = True