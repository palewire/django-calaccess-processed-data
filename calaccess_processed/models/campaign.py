#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing campaign finance tables derived from raw CAL-ACCESS data.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.managers import ProcessedDataManager


@python_2_unicode_compatible
class Election(models.Model):
    election_id = models.CharField(
        verbose_name="election identification number",
        max_length=3,
        null=False,
        blank=True,
        help_text="Election identification number",
    )
    election_year = models.IntegerField(
        verbose_name='year of election',
        db_index=True,
        null=False,
        help_text='Year of election',
    )
    election_type = models.CharField(
        verbose_name="election type",
        max_length=100,
        null=False,
        blank=True,
        help_text="Election type",
    )
    sort_index = models.IntegerField(
        verbose_name="sort index",
        null=False,
        help_text="The index value is used to preserve sorting of elections, \
        since multiple elections may occur in a year. A greater sort index \
        corresponds to a more recent election."
    )

    def __str__(self):
        return '{} {}'.format(self.election_year, self.election_type)


@python_2_unicode_compatible
class Race(models.Model):
    office_name = models.CharField(
        verbose_name="office name",
        max_length=100,
        null=False,
        blank=True,
        help_text="Office name",
    )
    # Preserve leading zeroes
    office_seat = models.CharField(
        verbose_name="office seat number",
        max_length=3,
        null=False,
        blank=True,
        help_text="Office seat number",
    )
    election = models.ForeignKey(
        'Election',
        null=True
    )

    def __str__(self):
        return '{} {}'.format(
            self.office_name,
            self.office_seat
        )


@python_2_unicode_compatible
class Candidate(models.Model):
    """
    Name, office/district/agency sought and contact info of each candidate.
    
    Derived from filers of Form 501 (Candidate Intention Statement).
    """
    filer_id = models.IntegerField(
        verbose_name="filer ID",
        null=False,
        help_text="Filer's unique id translated to numeric form (via "
                  "FILER_XREF_CD). In cases without an XREF translation, "
                  "the F501 filer_id is simply cast as an integer.",
    )
    title = models.CharField(
        verbose_name="name title",
        max_length=100,
        null=False,
        blank=True,
        help_text="Candidate's name title",
    )
    last_name = models.CharField(
        verbose_name="last name",
        max_length=200,
        null=False,
        # just a few don't even have a last name
        blank=True,
        help_text="Candidate's last name",
    )
    first_name = models.CharField(
        verbose_name="first name",
        max_length=45,
        null=False,
        blank=True,
        help_text="Candidate's first name",
    )
    middle_name = models.CharField(
        verbose_name="middle name",
        max_length=20,
        null=False,
        blank=True,
        help_text="Candidate's middle name",
    )
    name_suffix = models.CharField(
        verbose_name="name suffix",
        max_length=10,
        null=False,
        blank=True,
        help_text="Candidate's name suffix",
    )
    f501_filing_id = models.IntegerField(
        verbose_name="f501 filing id",
        db_index=True,
        null=False,
        help_text="Candidate's Form 501 filing identification number",
    )
    last_f501_amend_id = models.IntegerField(
        verbose_name="last f501 amendment id",
        db_index=True,
        null=False,
        help_text="Most recent amendment number to the candidate's Form 501",
    )
    # mostly numeric only values, but a few with leading 0
    controlled_committee_filer_id = models.CharField(
        verbose_name="controlled committee identification number",
        max_length=9,
        null=False,
        blank=True,
        # need to double check all of these are actually filer ids
        help_text="Candidate's controlled committee filer identification number",
    )
    office = models.CharField(
        max_length=80,
        verbose_name='office sought',
        null=False,
        blank=True,
        help_text='Office sought by candidate',
    )
    district = models.CharField(
        max_length=4,
        verbose_name='district',
        null=False,
        blank=True,
        help_text='District of office sought (if applicable)',
    )
    agency = models.CharField(
        max_length=200,
        verbose_name='agency sought',
        null=False,
        blank=True,
        help_text='Agency of office sought',
    )
    jurisdiction = models.CharField(
        max_length=30,
        verbose_name='jurisdiction',
        null=False,
        blank=True,
        default='',
        help_text='Jurisdiction (e.g., "LOCAL", "STATE") of the office sought',
    )
    party = models.CharField(
        max_length=200,
        verbose_name='party',
        null=False,
        blank=True,
        help_text="Candidate's political party",
    )
    election_year = models.IntegerField(
        verbose_name='year of election',
        db_index=True,
        null=True,
        help_text='Year of election',
    )
    city = models.CharField(
        max_length=200,
        verbose_name='city',
        null=False,
        blank=True,
        help_text="Candidate's city",
    )
    state = models.CharField(
        max_length=200,
        verbose_name='state',
        null=False,
        blank=True,
        help_text="Candidate's state",
    )
    zip_code = models.CharField(
        max_length=10,
        verbose_name='zip code',
        null=False,
        blank=True,
        help_text="Candidate's zip code",
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='phone number',
        null=False,
        blank=True,
        help_text="Candidate's phone number",
    )
    fax = models.CharField(
        max_length=20,
        verbose_name='fax number',
        null=False,
        blank=True,
        help_text="Candidate's fax number",
    )
    email = models.CharField(
        max_length=200,
        verbose_name='email address',
        null=False,
        blank=True,
        help_text="Candidate's email address",
    )

    race = models.ForeignKey(
        'Race',
        null=True
    )
    election = models.ForeignKey(
        'Election',
        null=True
    )

    objects = ProcessedDataManager()

    class Meta:
        """
        Meta model options.
        """
        app_label = 'calaccess_processed'

    def __str__(self):
        return '{} {}'.format(
            self.first_name,
            self.last_name
        )


@python_2_unicode_compatible
class F460Summary(models.Model):
    """
    Totals from the Summary Page of Form 460 (Recipient Committee Campaign 
    Statement) filings.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        db_index=True,
        null=False,
        help_text='Filing identification number',
    )
    amend_id = models.IntegerField(
        verbose_name='amendment id',
        db_index=True,
        null=False,
        help_text='Amendment identification number',
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

    objects = ProcessedDataManager()

    class Meta:
        verbose_name_plural = "f460_summaries"
        app_label = 'calaccess_processed'

    def __str__(self):
        return str(self.filing_id_raw)
