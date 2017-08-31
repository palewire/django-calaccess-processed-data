#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Campaign Disclosure Statements (Form 460).
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.base import CalAccessBaseModel


class Form460ScheduleFItemBase(CalAccessBaseModel):
    """
    Abstract base model for items reported on Schedule F of Form 460 filings.

    On Schedule F, campaign filers report unpaid bills for goods or services
    accrued during the period covered by the filing.
    """
    line_item = models.IntegerField(
        verbose_name='line item',
        help_text="Line number of the filing form where the unpaid bill is "
                  "itemized (from DEBT_CD.LINE_ITEM)",
    )
    PAYEE_CODE_CHOICES = (
        ('BNM', "Ballot measure's name/title"),
        ('COM', "Committee"),
        ('IND', "Individual"),
        ('OTH', "Other"),
        ('PTY', "Political Party"),
        ('RCP', "Recipient committee"),
        ('SCC', "Small Contributor Committee"),
        ('???', "Unknown value"),
    )
    payee_code = models.CharField(
        verbose_name='payee code',
        max_length=3,
        blank=True,
        choices=PAYEE_CODE_CHOICES,
        help_text='Code describing the payee (from DEBT_CD.ENTITY_CD)',
    )
    payee_committee_id = models.CharField(
        verbose_name='committee id',
        max_length=9,
        blank=True,
        help_text="Payee's filer identification number, if it is a "
                  "committee (from DEBT_CD.CMTE_ID)",
    )
    payee_title = models.CharField(
        verbose_name='payee title',
        max_length=10,
        blank=True,
        help_text='Name title of the payee (from DEBT_CD.PAYEE_NAMT)',
    )
    payee_lastname = models.CharField(
        verbose_name='payee lastname',
        max_length=200,
        blank=True,
        help_text='Last name of the payee or business name (from '
                  'DEBT_CD.PAYEE_NAML)',
    )
    payee_firstname = models.CharField(
        verbose_name='payee firstname',
        max_length=45,
        help_text='First name of the payee (from DEBT_CD.PAYEE_NAMF)',
    )
    payee_name_suffix = models.CharField(
        verbose_name='payee name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the payee (from DEBT_CD.PAYEE_NAMS)',
    )
    payee_city = models.CharField(
        verbose_name='payee city',
        max_length=30,
        blank=True,
        help_text='City of the payee (from DEBT_CD.PAYEE_CITY)',
    )
    payee_state = models.CharField(
        verbose_name='payee state',
        max_length=2,
        blank=True,
        help_text='State of the payee (from DEBT_CD.PAYEE_ST)',
    )
    payee_zip = models.CharField(
        verbose_name='payee zip',
        max_length=10,
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'payee (from DEBT_CD.PAYEE_ZIP4)',
    )
    treasurer_title = models.CharField(
        verbose_name='treasurer title',
        max_length=10,
        blank=True,
        help_text="Name title of the payee committee's treasurer (from "
                  "DEBT_CD.TRES_NAMT)",
    )
    treasurer_lastname = models.CharField(
        verbose_name='treasurer lastname',
        max_length=200,
        blank=True,
        help_text="Last name of the payee committee's treasurer (from "
                  "DEBT_CD.TRES_NAML)",
    )
    treasurer_firstname = models.CharField(
        verbose_name='treasurer firstname',
        max_length=45,
        help_text="First name of the payee committee's treasurer (from "
                  "DEBT_CD.TRES_NAMF)",
    )
    treasurer_name_suffix = models.CharField(
        verbose_name='treasurer name suffix',
        max_length=10,
        blank=True,
        help_text="Name suffix of the payee committee's treasurer (from "
                  "DEBT_CD.TRES_NAMS)",
    )
    treasurer_city = models.CharField(
        verbose_name='treasurer city',
        max_length=30,
        blank=True,
        help_text="City of the payee committee's treasurer (from DEBT_CD."
                  "TRES_CITY)",
    )
    treasurer_state = models.CharField(
        verbose_name='treasurer state',
        max_length=2,
        blank=True,
        help_text="State of the payee committee's treasurer (from DEBT_CD."
                  "TRES_ST)",
    )
    PAYMENT_CODE_CHOICES = (
        ('CMP', 'Campaign paraphernalia/miscellaneous'),
        ('CNS', 'Campaign consultants'),
        ('CTB', 'Contribution (if nonmonetary, explain)*'),
        ('CVC', 'Civic donations'),
        ('FIL', 'Candidate filing/ballot feeds'),
        ('FND', 'Fundraising events'),
        ('IKD', 'In-kind contribution (nonmonetary)'),
        ('IND', 'Independent expenditure supporting/opposing others (explain)*'),
        ('LEG', 'Legal defense'),
        ('LIT', 'Campaign literature and mailings'),
        ('LON', 'Loan'),
        ('MBR', 'Member communications'),
        ('MON', 'Monetary contribution'),
        ('MTG', 'Meetings and appearances'),
        ('OFC', 'Office expenses'),
        ('PET', 'Petition circulating'),
        ('PHO', 'Phone banks'),
        ('POL', 'Polling and survey research'),
        ('POS', 'Postage, delivery and messenger services'),
        ('PRO', 'Professional services (legal, accounting)'),
        ('PRT', 'Print ads'),
        ('RAD', 'Radio airtime and production costs'),
        ('RFD', 'Returned contributions'),
        ('SAL', 'Campaign workers salaries'),
        ('TEL', 'T.V. or cable airtime and production costs'),
        ('TRC', 'Candidate travel, lodging and meals (explain)'),
        ('TRS', 'Staff/spouse travel, lodging and meals (explain)'),
        ('TSF', 'Transfer between committees of the same candidate/sponsor'),
        ('VOT', 'Voter registration'),
        ('WEB', 'Information technology costs (internet, e-mail)'),
        ('???', "Unknown value"),
    )
    payment_code = models.CharField(
        verbose_name='payment code',
        max_length=3,
        blank=True,
        choices=PAYMENT_CODE_CHOICES,
        help_text='Code describing the payment (from DEBT_CD.EXPN_CODE)',
    )
    payment_description = models.CharField(
        verbose_name="payment description",
        max_length=400,
        blank=True,
        help_text="Purpose of payment and/or description/explanation (from "
                  "DEBT_CD.EXPN_DSCR)",
    )
    begin_balance = models.DecimalField(
        verbose_name="begin balance",
        decimal_places=2,
        max_digits=14,
        help_text="Outstanding balance at the beginning of period covered by "
                  "the filing (from DEBT_CD.BEG_BAL)",
    )
    amount_paid = models.DecimalField(
        decimal_places=2,
        max_digits=14,
        help_text='Amount paid this period (from DEBT_CD.AMT_PAID)'
    )
    amount_incurred = models.DecimalField(
        verbose_name="amount incurred",
        decimal_places=2,
        max_digits=14,
        help_text='Amount incurred this period (from DEBT_CD.AMT_INCUR)',
    )
    end_balance = models.DecimalField(
        verbose_name="end balance",
        decimal_places=2,
        max_digits=14,
        help_text="Outstanding balance at the end of period covered by the "
                  "filing (from DEBT_CD.END_BAL)",
    )
    transaction_id = models.CharField(
        verbose_name='transaction id',
        max_length=20,
        help_text='Identifies a unique transaction across versions of the a '
                  'given Form 460 filing (from DEBT_CD.TRAN_ID)',
    )
    parent_transaction_id = models.CharField(
        verbose_name='parent transaction id',
        max_length=20,
        blank=True,
        help_text='Refers to a parent transaction itemized on the same Form '
                  '460 filing (from DEBT_CD.BAKREF_TID)',
    )
    memo_reference_number = models.CharField(
        verbose_name='memo reference number',
        max_length=20,
        blank=True,
        help_text="A value assigned by the filer which refers to the item's"
                  "footnote in the TEXT_MEMO_CD table (from DEBT_CD."
                  "MEMO_REFNO)",
    )
    memo_code = models.BooleanField(
        verbose_name='memo_code',
        default=False,
        help_text="Memo amount flag (from DEBT_CD.MEMO_CODE)"
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleFItem(Form460ScheduleFItemBase):
    """
    Accrued expenses of campaign filers.

    These transactions are itemized on Schedule F of the most recent version
    of each Form 460 filing. For accrued expenses itemized on any version of
    of any Form 460 filing, see Form460ScheduleFItemVersion.

    Derived from DEBT_CD records.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_f_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the '
                  'payment was reported (from DEBT_CD.FILING_ID)',
    )

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing',
            'line_item',
        ),)
        verbose_name = "Form 460 (Campaign Disclosure) Schedule F item"

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleFItemVersion(Form460ScheduleFItemBase):
    """
    Every version of each accrued expense of a campaign filer.

    For accrued expenses itemized on Schedule F of the most recent version of
    each Form 460 filing, see Form460ScheduleGItem.

    Derived from DEBT_CD records.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_f_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the Schedule F items'
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
        verbose_name = "Form 460 (Campaign Disclosure) Schedule F item version"

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )
