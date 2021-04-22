#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing Part 2 data from Schedule 496, the Late Independent Expenditure Reports.

More about the filing: https://calaccess.californiacivicdata.org/documentation/calaccess-forms/f496/
"""
from django.db import models
from calaccess_processed_filings.models.base import FilingBaseModel


class Form496Part2ItemBase(FilingBaseModel):
    """
    Abstract base model for items reported on Part 2 of Schedule 496 filings.

    On Part 2 of Schedule 496, campaign filers are required to report
    independent expenditures made in the 90 days leading up to an election.
    """
    line_item = models.IntegerField(
        verbose_name='line item',
        db_index=True,
        null=False,
        help_text='Line number of the filing form where the transaction is '
                  'itemized (from S496_CD.LINE_ITEM)',
    )
    expense_date = models.DateField(
        verbose_name="expense date",
        null=True,
        help_text="Date or expense (from S496_CD.EXP_DATE)",
    )
    amount = models.DecimalField(
        verbose_name='amount',
        decimal_places=2,
        max_digits=14,
        help_text="Amount paid to the payee in the period covered by the "
                  "filing (from S496_CD.AMOUNT)",
    )
    transaction_id = models.CharField(
        verbose_name='transaction id',
        max_length=20,
        db_index=True,
        help_text='Identifies a unique transaction across versions of the a '
                  'given Schedule 496 filing (from S496_CD.TRAN_ID)'
    )
    payment_description = models.CharField(
        verbose_name="payment description",
        max_length=400,
        blank=True,
        help_text="Purpose of payment and/or description/explanation (from S496_CD.EXPN_DSCR)",
    )
    memo_code = models.CharField(
        verbose_name='memo code',
        max_length=500,
        blank=True,
        help_text="A description offered by the filer",
    )
    memo_reference_number = models.CharField(
        verbose_name='memo reference number',
        max_length=20,
        blank=True,
        help_text='Reference number for the memo attached to the transaction '
                  '(from S496_CD.MEMO_REFNO)',
    )

    class Meta:
        """
        Model options.
        """
        app_label = 'calaccess_processed_filings'
        abstract = True


class Form496Part2Item(Form496Part2ItemBase):
    """
    Late independent expenditures made by campaign filers.

    These transactions are itemized on Part 2 of the most recent version
    of each Schedule 496 filing.
    """
    filing = models.ForeignKey(
        'Form496Filing',
        related_name='independent_expenditures_made',
        db_constraint=False,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Unique identification number for the Schedule 496 filing (from S496_CD.FILING_ID)',
    )

    class Meta:
        """
        Model options.
        """
        app_label = 'calaccess_processed_filings'
        unique_together = ((
            'filing',
            'line_item',
        ),)
        verbose_name = "Form 496 (Late Independent Expenditure) Part 2 item"

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


class Form496Part2ItemVersion(Form496Part2ItemBase):
    """
    Every version of each late independent expenditure made by a campaign filer.
    """
    filing_version = models.ForeignKey(
        'Form496FilingVersion',
        related_name='independent_expenditures_made',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Schedule 496 that includes the given expenditure'
    )

    class Meta:
        """
        Model options.
        """
        app_label = 'calaccess_processed_filings'
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)
        verbose_name = "Form 496 (Late Independent Expenditure) Part 2 item version"

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )
