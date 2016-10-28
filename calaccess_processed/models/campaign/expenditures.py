#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing campaign-related transactions derived from raw CAL-ACCESS data.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.managers import ProcessedDataManager


class PaymentMadeBase(models.Model):
    """
    Abstract base model for payments made by or on behalf of campaign filers.

    These transactions are itemized on Schedules E and G of Form 460 filings
    and stored in the EXPN_CD table.
    """
    line_item = models.IntegerField(
        verbose_name='line item',
        help_text="Line number of the filing form where the payment is "
                  "itemized (from EXPN_CD.LINE_ITEM)",
    )
    PAYEE_CODE_CHOICES = (
        ('BNM', "Ballot measure's name/title"),
        ('CAO', "Candidate/officeholder"),
        ('COM', "Committee"),
        ('IND', "Individual"),
        ('MBR', "Member of Associaton"),
        ('OFF', "Officer"),
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
        help_text='Code describing the payee (from EXPN_CD.ENTITY_CD)',
    )
    payee_committee_id = models.CharField(
        verbose_name='committee id',
        max_length=9,
        blank=True,
        help_text="payee's filer identification number, if it is a "
                  "committee (from EXPN_CD.CMTE_ID)",
        )
    payee_title = models.CharField(
        verbose_name='payee title',
        max_length=10,
        blank=True,
        help_text='Name title of the payee (from EXPN_CD.PAYEE_NAMT)',
    )
    payee_lastname = models.CharField(
        verbose_name='payee lastname',
        max_length=200,
        blank=True,
        help_text='Last name of the payee or business name (from '
                  'EXPN_CD.PAYEE_NAML)',
    )
    payee_firstname = models.CharField(
        verbose_name='payee firstname',
        max_length=45,
        help_text='First name of the payee (from EXPN_CD.PAYEE_NAMF)',
    )
    payee_name_suffix = models.CharField(
        verbose_name='payee name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the payee (from EXPN_CD.PAYEE_NAMS)',
    )
    payee_city = models.CharField(
        verbose_name='payee city',
        max_length=30,
        blank=True,
        help_text='City of the payee (from EXPN_CD.PAYEE_CITY)',
    )
    payee_state = models.CharField(
        verbose_name='payee state',
        max_length=2,
        blank=True,
        help_text='State of the payee (from EXPN_CD.PAYEE_ST)',
    )
    payee_zip = models.CharField(
        verbose_name='payee zip',
        max_length=10,
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'payee (from EXPN_CD.PAYEE_ZIP4)',
    )
    treasurer_title = models.CharField(
        verbose_name='treasurer title',
        max_length=10,
        blank=True,
        help_text="Name title of the payee committee's treasurer (from "
                  "EXPN_CD.TRES_NAMT)",
    )
    treasurer_lastname = models.CharField(
        verbose_name='treasurer lastname',
        max_length=200,
        blank=True,
        help_text="Last name of the payee committee's treasurer (from "
                  "EXPN_CD.TRES_NAML)",
    )
    treasurer_firstname = models.CharField(
        verbose_name='treasurer firstname',
        max_length=45,
        help_text="First name of the payee committee's treasurer (from "
                  "EXPN_CD.TRES_NAMF)",
    )
    treasurer_name_suffix = models.CharField(
        verbose_name='treasurer name suffix',
        max_length=10,
        blank=True,
        help_text="Name suffix of the payee committee's treasurer (from "
                  "EXPN_CD.TRES_NAMS)",
    )
    treasurer_city = models.CharField(
        verbose_name='treasurer city',
        max_length=30,
        blank=True,
        help_text="City of the payee committee's treasurer (from EXPN_CD."
                  "TRES_CITY)",
    )
    treasurer_state = models.CharField(
        verbose_name='treasurer state',
        max_length=2,
        blank=True,
        help_text="State of the payee committee's treasurer (from EXPN_CD."
                  "TRES_ST)",
    )
    treasurer_zip = models.CharField(
        verbose_name='treasurer zip',
        max_length=10,
        blank=True,
        help_text="Zip code (usually zip5, sometimes zip9) of the payee "
                  "committee's treasurer (from EXPN_CD.TRES_ZIP4)",
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
        help_text='Code describing the payment (from EXPN_CD.EXPN_CODE)',
    )
    payment_description = models.CharField(
        verbose_name="payment description",
        max_length=400,
        blank=True,
        help_text="Purpose of payment and/or description/explanation (from "
                  "EXPN_CD.AMOUNT)",
    )
    amount = models.DecimalField(
        verbose_name='amount',
        decimal_places=2,
        max_digits=14,
        help_text="Amount paid to the payee in the period covered by the "
                  "filing (from EXPN_CD.AMOUNT)",
    )
    payment_date = models.DateField(
        verbose_name="expense date",
        null=True,
        help_text="Date payment made (from EXPN_CD.EXPN_DATE)",
    )
    check_number = models.CharField(
        verbose_name='expense check number',
        max_length=20,
        blank=True,
        help_text="Optional check number for the payment made by the campaign "
                  "filer (from EXPN_CD.EXPN_CHKNO)",
    )
    transaction_id = models.CharField(
        verbose_name='transaction id',
        max_length=20,
        help_text='Identifies a unique transaction across versions of the a '
                  'given Form 460 filing (from EXPN_CD.TRAN_ID)',
    )
    parent_transaction_id = models.CharField(
        verbose_name='parent transaction id',
        max_length=20,
        blank=True,
        help_text='Refers to a parent transaction itemized on the same Form '
                  '460 filing, though possibly on a different schedule (from '
                  'EXPN_CD.BAKREF_TID)',
    )
    informational_memo = models.BooleanField(
        verbose_name='informational_memo',
        max_length=1,
        default=False,
        help_text="Date/amount are informational only (from EXPN_CD.MEMO_CODE)"
    )
    memo_reference_number = models.CharField(
        verbose_name='memo reference number',
        max_length=20,
        blank=True,
        help_text="A value assigned by the filer which refers to the item's" 
                  "footnote in the TEXT_MEMO_CD table (from "
                  "EXPN_CD.MEMO_REFNO)",
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class PaymentMade(PaymentMadeBase):
    """
    Payments made by campaign filers.

    These transactions are itemized on Schedule E of the most recent amendment
    to each Form 460 filing. For payments itemized on any version of any Form
    460 filing, see paymentsmadeversion.

    Does not include:
    * Interest paid on loans received
    * Loans made to others
    * Payments by agents and independent contractors
    * Transfers of campaign funds into savings accounts
    * Certificates of deposit
    * Money market accounts
    * Purchases of other assets that can readily be converted to cash

    Derived from EXPN_CD records where FORM_TYPE is 'E'.
    """
    filing = models.ForeignKey(
        'Form460',
        related_name='itemized_payments_made',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the '
                  'payment was reported (from RCPT_CD.FILING_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class PaymentMadeVersion(PaymentMadeBase):
    """
    Every version of the payments by campaign filers.

    For payments itemized on Schedule E of the most recent version of each Form
    460 filing, see paymentsmade.

    Does not include:
    * Interest paid on loans received
    * Loans made to others
    * Payments by agents and independent contractors
    * Transfers of campaign funds into savings accounts
    * Certificates of deposit
    * Money market accounts
    * Purchases of other assets that can readily be converted to cash

    Derived from EXPN_CD records where FORM_TYPE is 'E'.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        null=False,
        help_text='Unique identification number for the Form 460 filing ('
                  'from EXPN_CD.FILING_ID)',
    )
    amend_id = models.IntegerField(
        verbose_name='amendment id',
        null=False,
        help_text='Identifies the version of the Form 460 filing, with 0 '
                  'representing the initial filing (from EXPN_CD.AMEND_ID)',
    )
    filing_version = models.ForeignKey(
        'Form460Version',
        related_name='itemized_payments_made',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the payment made'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_id',
            'amend_id',
            'line_item',
        ),)
        index_together = ((
            'filing_id',
            'amend_id',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (self.filing_id, self.amend_id, self.line_item)
