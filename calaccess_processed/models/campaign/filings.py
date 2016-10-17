#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing campaign-related filings derived from raw CAL-ACCESS data.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.managers import ProcessedDataManager

class CampaignFinanceFilingBase(models.Model):
    """
    Base and abstract model for campaign finance-related filings.
    """
    date_filed = models.DateField(
        verbose_name='date filed',
        db_index=True,
        null=False,
        help_text="Date this report was filed, according to the filer "
                  "(from CVR_CAMPAIGN_DISCLOSURE.RPT_DATE)",
    )
    filer_id = models.IntegerField(
        verbose_name='filer id',
        db_index=True,
        null=False,
        help_text="Numeric filer identification number (from FILER_XREF.FILER_ID)",
    )
    filer_lastname = models.CharField(
        verbose_name='filer last name',
        max_length=200,
        null=False,
        blank=False,
        help_text="Last name of filer (from CVR_CAMPAIGN_DISCLOSURE.FILER_NAML)",
    )
    filer_firstname = models.CharField(
        verbose_name="filer first name",
        max_length=45,
        null=False,
        blank=True,
        help_text="First name of the filer (from "
                  "CVR_CAMPAIGN_DISCLOSURE.FILER_NAMF)",
    )
    election_date = models.DateField(
        verbose_name='election date',
        db_index=True,
        null=True,
        help_text="Date of the election in which the filer is participating "
                  "(from CVR_CAMPAIGN_DISCLOSURE.ELECT_DATE)",
    )

    class Meta:
        app_label = 'calaccess_processed'
        abstract = True


class F460Base(CampaignFinanceFilingBase):
    """
    Base and abstract model for Form 460 filings.
    """
    from_date = models.DateField(
        verbose_name='from date',
        db_index=True,
        null=False,
        help_text="The first date of the filing period covered by the statement "
                  "(from CVR_CAMPAIGN_DISCLOSURE.FROM_DATE)",
    )
    thru_date = models.DateField(
        verbose_name='thru date',
        db_index=True,
        null=False,
        help_text="The last date of the filing period covered by the statement "
                  "(from CVR_CAMPAIGN_DISCLOSURE.THRU_DATE)",
    )
    monetary_contributions = models.IntegerField(
        verbose_name='monetary contributions',
        null=True,
        help_text="Total monetary contributions (from line 1, column A)",
    )
    loans_received = models.IntegerField(
        verbose_name='loans received',
        null=True,
        help_text="Total loans received (from line 2, column A)",
    )
    subtotal_cash_contributions = models.IntegerField(
        verbose_name='subtotal cash contributions',
        null=True,
        help_text="Monetary contributions and loans received combined (from "
                  "line 3, column A)",
    )
    nonmonetary_contributions = models.IntegerField(
        verbose_name='nonmonetary contributions',
        null=True,
        help_text="Non-monetary contributions (from line 4, column A)",
    )
    total_contributions = models.IntegerField(
        verbose_name='total contributions',
        null=True,
        help_text="Total contributions (from line 5, column A)",
    )
    payments_made = models.IntegerField(
        verbose_name='payments made',
        null=True,
        help_text="Payments made (from line 6, column A)",
    )
    loans_made = models.IntegerField(
        verbose_name='loans made',
        null=True,
        help_text="Loans made (from line 7, column A)",
    )
    subtotal_cash_payments = models.IntegerField(
        verbose_name='subtotal cash payments',
        null=True,
        help_text="Sub-total of cash payments (from line 8, column A)",
    )
    unpaid_bills = models.IntegerField(
        verbose_name='unpaid bills',
        null=True,
        help_text="Unpaid bills / accrued expenses (from line 9, column A)",
    )
    nonmonetary_adjustment = models.IntegerField(
        verbose_name='nonmonetary adjustment',
        null=True,
        help_text="Non-monetary adjustment (from line 10, column A), which is "
                  "equal to the total of non-monetary contributions",
    )
    total_expenditures_made = models.IntegerField(
        verbose_name='total expenditures made',
        null=True,
        help_text="Total expenditures made (from line 11, column A)",
    )
    begin_cash_balance = models.IntegerField(
        verbose_name='begin cash balance',
        null=True,
        help_text="Beginning cash balance (from line 12), which is equal to "
                  "the Ending Cash Balance (line 16) reported on the summary "
                  "page of the previous Form 460 filing"
    )
    cash_receipts = models.IntegerField(
        verbose_name='cash receipts',
        null=True,
        help_text="Cash receipts (from line 13)",
    )
    miscellaneous_cash_increases = models.IntegerField(
        verbose_name='miscellaneous cash increases',
        null=True,
        help_text="Miscellaneous cash increases (from line 14)",
    )
    cash_payments = models.IntegerField(
        verbose_name='cash payments',
        null=True,
        help_text="Cash payments (from line 15)",
    )
    ending_cash_balance = models.IntegerField(
        verbose_name='ending cash balance',
        null=True,
        help_text="Ending cash balance (from line 16)",
    )
    loan_guarantees_received = models.IntegerField(
        verbose_name='loan guarantees received',
        null=True,
        help_text="Loan guarantees received (from line 17)",
    )
    cash_equivalents = models.IntegerField(
        verbose_name='cash equivalents',
        null=True,
        help_text="Cash equivalents (from line 18), which includes investments "
                  "that can't be readily converted to cash, such as outstanding "
                  "loans the committee has made to others"
    )
    outstanding_debts = models.IntegerField(
        verbose_name='outstanding debts',
        null=True,
        help_text="Outstanding debts on loans owed by the committee (from line "
                  "19)",
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class F460Filing(F460Base):
    """
    The most recent version of each Form 460 (Campaign Disclosure Statement) 
    filing by recipient committees.

    Includes information from the cover sheet and summary page of the most 
    recent amendment to each filing. All versions of Form 460 filings can be
    found in f460version.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        primary_key=True,
        db_index=True,
        null=False,
        help_text='Unique identification number for the Form 460 filing ('
                  'from CVR_CAMPAIGN_DISCLOSURE_CD.FILING_ID)',
    )
    amendment_count = models.IntegerField(
        verbose_name='Count amendments',
        db_index=True,
        null=False,
        help_text='Number of amendments to the Form 460 filing (from '
                  'maximum value of CVR_CAMPAIGN_DISCLOSURE_CD.AMEND_ID)',
    )

    objects = ProcessedDataManager()

    def __str__(self):
        return str(self.filing_id)


@python_2_unicode_compatible
class F460FilingVersion(F460Base):
    """
    Every version of each Form 460 (Campaign Disclosure Statement) filing by
    recipient committees.

    Includes information found on the cover sheet and summary page of each
    amendment. For the most recent version of each filing, see f460filing.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        db_index=True,
        null=False,
        help_text='Unique identification number for the Form 460 filing ('
                  'from CVR_CAMPAIGN_DISCLOSURE_CD.FILING_ID)',
    )
    amend_id = models.IntegerField(
        verbose_name='amendment id',
        db_index=True,
        null=False,
        help_text='Identifies the version of the Form 497 filing, with 0 '
                  'representing the initial filing (from CVR_CAMPAIGN_'
                  'DISCLOSURE_CD.AMEND_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_id',
            'amend_id',
        ),)

    def __str__(self):
        return str(self.filing_id)


@python_2_unicode_compatible
class S497Filing(CampaignFinanceFilingBase):
    """
    The most recent version of each Form 497 (Late Contribution Report) 
    filing by recipient committees.

    Includes information from the cover sheet of the most recent amendment to 
    each filing. All versions of Form 497 filings can befound in f497version.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        primary_key=True,
        db_index=True,
        null=False,
        help_text='Unique identification number for the Schedule 497 filing ('
                  'from CVR_CAMPAIGN_DISCLOSURE_CD.FILING_ID)',
    )
    amendment_count = models.IntegerField(
        verbose_name='Count amendments',
        db_index=True,
        null=False,
        help_text='Number of amendments to the Form 497 filing (from '
                  'maximum value of CVR_CAMPAIGN_DISCLOSURE_CD.AMEND_ID)',
    )

    objects = ProcessedDataManager()

    def __str__(self):
        return str(self.filing_id)


@python_2_unicode_compatible
class S497FilingVersion(CampaignFinanceFilingBase):
    """
    Every version of each Form 497 (Late Contribution Report) filing by
    recipient committees.

    Includes information found on the cover sheet of each amendment. For the 
    most recent version of each filing, see f497filing.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        db_index=True,
        null=False,
        help_text='Unique identification number for the Schedule 497 filing ('
                  'from S497_CD.FILING_ID)',
    )
    amend_id = models.IntegerField(
        verbose_name='amendment id',
        db_index=True,
        null=False,
        help_text='Identifies the version of the Schedule 497 filing, with 0 '
                  'representing the initial filing (from CVR_CAMPAIGN_'
                  'DISCLOSURE_CD.AMEND_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_id',
            'amend_id',
        ),)

    def __str__(self):
        return str(self.filing_id)
