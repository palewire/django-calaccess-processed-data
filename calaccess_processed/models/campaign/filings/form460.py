#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Campaign Disclosure Statements (Form 460).
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.managers import ProcessedDataManager
from calaccess_processed.models.campaign.filings import (
    CampaignFinanceFilingBase,
    CampaignContributionBase,
    CampaignExpenditureItemBase,
    CampaignExpenditureSubItemBase,
)


class Form460FilingBase(CampaignFinanceFilingBase):
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
class Form460Filing(Form460FilingBase):
    """
    The most recent version of each Form 460 filing by recipient committees.

    Form 460 is the Campaign Disclosure Statement filed by all recipient
    committees, including:
    * Candidates, officeholders and their controlled committees
    * Primarily formed ballot measure committees
    * Primarily formed candidate/of ceholder committees
    * General purpose committees

    Recipient committes can use Form 460 to file:
    * Pre-election statements
    * Semi-annual statements
    * Quarterly statements
    * Termination statements
    * Special odd-year report
    
    Includes information from the cover sheet and summary page of the most 
    recent version of each Form 460 filing. All versions of the filings can be
    found in Form460FilingVersion.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        primary_key=True,
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

    class Meta:
        index_together = ((
            'filing_id',
            'amendment_count',
        ),)

    def __str__(self):
        return str(self.filing_id)


@python_2_unicode_compatible
class Form460FilingVersion(Form460FilingBase):
    """
    Every version of each Form 460 (Campaign Disclosure Statement) filing by
    recipient committees.

    Includes information found on the cover sheet and summary page of each
    version of each Form 460 filing. For the most recent version of each filing,
    see Form460Filing.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='versions',
        db_constraint=False,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Unique identification number for the Form 460 filing ('
                  'from CVR_CAMPAIGN_DISCLOSURE_CD.FILING_ID)',
    )
    amend_id = models.IntegerField(
        verbose_name='amendment id',
        null=False,
        help_text='Identifies the version of the Form 497 filing, with 0 '
                  'representing the initial filing (from CVR_CAMPAIGN_'
                  'DISCLOSURE_CD.AMEND_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing',
            'amend_id',
        ),)
        index_together = ((
            'filing',
            'amend_id',
        ),)

    def __str__(self):
        return '%s-%s' % (self.filing, self.amend_id)


class Form460ScheduleAItemBase(CampaignContributionBase):
    """
    Abstract base model for items reported on Schedule A of Form 460 filings.

    On Schedule A, campaign filers are required to itemize monetary
    contributions received during the period covered by the filing.
    """
    amount = models.DecimalField(
        verbose_name='amount',
        decimal_places=2,
        max_digits=14,
        help_text="Amount received from the contributor in the period covered "
                  "by the filing (from RCPT_CD.AMOUNT)"
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleAItem(Form460ScheduleAItemBase):
    """
    Monetary contributions received by campaign filers.

    These transactions are itemized on Schedule A of the most recent version
    to each Form 460 filing. For monetary contributions itemized on any version
    of any Form 460 filing, see Form460ScheduleAItemVersion.

    Also includes contributions transferred to special election commitees,
    formerly itemized on Schedule A-1. 

    Derived from RCPT_CD records where FORM_TYPE is 'A' or 'A-1'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_a_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the monetary'
                  ' contribution was reported (from RCPT_CD.FILING_ID)',
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
class Form460ScheduleAItemVersion(Form460ScheduleAItemBase):
    """
    Every version of the monetary contributions received by campaign filers.

    For monetary contributions itemized on Schedule A of the most recent
    version of each Form 460 filing, see Form460ScheduleAItem.

    Derived from RCPT_CD records where FORM_TYPE is 'A' or 'A-1'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_a_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the received contribution'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


class Form460ScheduleB1ItemBase(models.Model):
    """
    Abstract base model for items reported on Schedule B, Part 1, of Form 460.

    On Schedule B, campaign filers are required to report loans received or 
    outstanding during the period covered by the filing.
    """
    line_item = models.IntegerField(
        verbose_name='line item',
        help_text="Line number of the filing form where the loan is "
                  "itemized (from LOAN_CD.LINE_ITEM)",
    )
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
    is_guarantor = models.BooleanField(
        verbose_name='is guarantor',
        default=False,
        help_text="Indicates if the lender is guarantor for the line or line "
                  "of credit. Until 2001, loans listed on Schedule B Part 1 of"
                  " Form 460 were coded as orginator from a \"Lender\" or "
                  "\"Guarantor\". However, this field is blank for records "
                  "dated after 2001 (from LOAN_CD.LOAN_TYPE)."
    )
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
        help_text="(from LOAN_CD.LOAN_AMT7)"
    )
    interest_rate = models.CharField(
        verbose_name='interest rate',
        max_length=30,
        blank=True,
        help_text='Interest rate of the loan. This is sometimes expressed as a '
                  'decimal (e.g., 0.10) and other times as a percent (e.g., '
                  '10.0% (from LOAN_CD.LOAN_RATE)'
    )
    original_amount = models.DecimalField(
        verbose_name='original amount',
        decimal_places=2,
        max_digits=14,
        help_text="Original amount loaned by the lender to the campaign filer "
                  "(from LOAN_CD.LOAN_AMT8)"
    )
    date_incurred = models.DateField(
        verbose_name='',
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
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleB1Item(Form460ScheduleB1ItemBase):
    """
    Outstanding loans received by campaign filers.

    These transactions are itemized on Schedule B, Part 1, of the most recent
    version to each Form 460 filing. For nonmonetary contributions itemized on
    any version of any Form 460 filing, see Form460ScheduleB1ItemVersion.

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

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleB1ItemVersion(Form460ScheduleB1ItemBase):
    """
    Every version of the outstanding loans received by campaign filers.

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

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


class Form460ScheduleCItemBase(CampaignContributionBase):
    """
    Abstract base model for items reported on Schedule C of Form 460 filings.

    On Schedule C, campaign filers are required to itemize nonmonetary
    contributions received during the period covered by the filing.
    """
    fair_market_value = models.DecimalField(
        verbose_name='fair market value',
        decimal_places=2,
        max_digits=14,
        help_text="Amount it would cost to purchase the donated goods or "
                  "services on the open market (from RCPT_CD.AMOUNT)"
    )
    contribution_description = models.CharField(
        max_length=90,
        blank=True,
        help_text="Description of the contributed goods or services (from "
                  "RCPT_CD.CTRIB_DSCR)"
    )
    
    class Meta:
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleCItem(Form460ScheduleCItemBase):
    """
    Nonmonetary contributions received by campaign filers.

    These transactions are itemized on Schedule C of the most recent version
    to each Form 460 filing. For nonmonetary contributions itemized on any 
    version of any Form 460 filing, see Form460ScheduleCItemVersion.

    Derived from RCPT_CD records where FORM_TYPE is 'C'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_c_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the monetary'
                  ' contribution was reported (from RCPT_CD.FILING_ID)',
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
class Form460ScheduleCItemVersion(Form460ScheduleCItemBase):
    """
    Every version of the nonmonetary contributions received by campaign filers.

    For nonmonetary contributions itemized on Schedule C of the most recent
    version of each Form 460 filing, see Form460ScheduleCItem.

    Derived from RCPT_CD records where FORM_TYPE is 'C'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_c_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the received contribution'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


class Form460ScheduleDItemBase(CampaignExpenditureItemBase):
    """
    Abstract base model for items reported on Schedule D of Form 460 filings.

    On Schedule D, campaign filers are required to summarize contributions
    and independent expenditures in support or opposition to other candidates
    and ballot measures.
    """
    cumulative_election_amount = models.DecimalField(
        decimal_places=2,
        max_digits=14,
        null=True,
        help_text="If the candidate is subject to contribution limits, the "
                  "cumulative amount given by the filer during the election "
                  "cycle as of the Form 460's filing date (from EXPN_CD."
                  "CUM_OTH)"
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleDItem(Form460ScheduleDItemBase):
    """
    Contributions and expenditures supporting/opposing other candidates and ballot measures.

    These transactions are itemized on Schedule D of the most recent version
    to each Form 460 filing. For payments itemized on any version of any Form
    460 filing, see Form460ScheduleDItemVersion.

    Derived from EXPN_CD records where FORM_TYPE is 'D'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_d_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the '
                  'payment was reported (from EXPN_CD.FILING_ID)',
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
class Form460ScheduleDItemVersion(Form460ScheduleDItemBase):
    """
    Every version of the payments made on behalf of campaign filers.

    For payments itemized on Schedule D of the most recent version of each Form
    460 filing, see Form460ScheduleDItem.

    Derived from EXPN_CD records where FORM_TYPE is 'D'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_d_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the payment made'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


@python_2_unicode_compatible
class Form460ScheduleEItem(CampaignExpenditureItemBase):
    """
    Payments made by campaign filers, itemized on Form 460 Schedule E.

    These transactions are itemized on Schedule E of the most recent version 
    of each Form 460 filing. For payments itemized on any version of any filing,
    see Form460ScheduleEItemVersion.

    Does not include:
    * Interest paid on loans received
    * Loans made to others
    * Transfers of campaign funds into savings accounts
    * Payments made by agents or contractors on behalf of the filer
    * Certificates of deposit
    * Money market accounts
    * Purchases of other assets that can readily be converted to cash

    Derived from EXPN_CD records where FORM_TYPE is 'E'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_e_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the '
                  'payment was reported (from EXPN_CD.FILING_ID)',
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
class Form460ScheduleEItemVersion(CampaignExpenditureItemBase):
    """
    Every version of the payments made, itemized on Form 460 Schedule E.

    For payments itemized on the most recent version of each Form 460 filing,
    see Form460scheduleeitem.

    Does not include:
    * Interest paid on loans received
    * Loans made to others
    * Transfers of campaign funds into savings accounts
    * Payments made by agents or contractors on behalf of the filer
    * Certificates of deposit
    * Money market accounts
    * Purchases of other assets that can readily be converted to cash

    Derived from EXPN_CD records where FORM_TYPE is 'E'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_e_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the payment made'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


@python_2_unicode_compatible
class Form460ScheduleESubItem(CampaignExpenditureSubItemBase):
    """
    Sub-items of payments made by campaign filers.

    These transactions are itemized on Schedule E of the most recent version
    of each Form 460 filing. For payments sub-itemized on any version of
    any Form 460 filing, see Form460ScheduleESubItemVersion.

    A sub-item is a transaction where the amount is lumped into another 
    "parent" payment reported elsewhere on the filing.

    Includes:
    * Payments supporting or opposing other candidates, ballot measures 
    or committees, which are summarized on Schedule D
    * Payments made to vendors over $100 included in credit card payments
    * Payments made by agents or independent contractors on behalf of the 
    campaign filer which were reported on Schedule E instead of G
    * Payments made on the accrued expenses reported on Schedule F

    Derived from EXPN_CD records where FORM_TYPE is 'E' and MEMO_CODE is not
    blank.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_e_subitems',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the '
                  'payment was reported (from EXPN_CD.FILING_ID)',
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
class Form460ScheduleESubItemVersion(CampaignExpenditureSubItemBase):
    """
    Every version of the sub-items of payments by campaign filers.

    For payments sub-itemized on Schedule E of the most recent version of each
    Form 460 filing, see Form460scheduleesubitem.

    A sub-item is a transaction where the amount is lumped into another
    "parent" payment reported elsewhere on the filing.

    Includes:
    * Payments supporting or opposing other candidates, ballot measures 
    or committees, which are summarized on Schedule D
    * Payments made to vendors over $100 included in credit card payments
    * Payments made by agents or independent contractors on behalf of the 
    campaign filer which were reported on Schedule E instead of G
    * Payments made on the accrued expenses reported on Schedule F

    Derived from EXPN_CD records where FORM_TYPE is 'E' and MEMO_CODE is not
    blank.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_e_subitems',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the payment made'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


class Form460ScheduleFItemBase(models.Model):
    """
    Abstract base model for items reported on Schedule F of Form 460.

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
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleFItem(Form460ScheduleFItemBase):
    """
    Accrued expenses of campaign filers.

    These transactions are itemized on Schedule F of the most recent version
    to each Form 460 filing. For accrued expenses itemized on any version of
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

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleFItemVersion(Form460ScheduleFItemBase):
    """
    Every version of the accrued expenses of campaign filers.

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

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


class Form460ScheduleGItemBase(CampaignExpenditureSubItemBase):
    """
    Abstract base model for items reported on Schedule G of Form 460 filings.

    On Schedule G, campaign filers are required to itemize payments made on 
    their behalf by agents or contractors during the period covered by the
    filing.
    """
    agent_title = models.CharField(
        verbose_name='agent title',
        max_length=10,
        blank=True,
        help_text='Name title of the agent (from EXPN_CD.AGENT_NAMT)',
    )
    agent_lastname = models.CharField(
        verbose_name='agent lastname',
        max_length=200,
        blank=True,
        help_text='Last name of the agent or business name (from '
                  'EXPN_CD.AGENT_NAML)',
    )
    agent_firstname = models.CharField(
        verbose_name='agent firstname',
        max_length=45,
        help_text='First name of the agent (from EXPN_CD.AGENT_NAMF)',
    )
    agent_name_suffix = models.CharField(
        verbose_name='agent name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the agent (from EXPN_CD.AGENT_NAMS)',
    )
    PARENT_SCHEDULE_CHOICES = (
        ('E', 'Schedule E: Payments Made'),
        ('F', 'Schedule F: Accrued Expenses (Unpaid Bills)')
    )
    parent_schedule = models.CharField(
        max_length=1,
        blank=True,
        help_text="Indicates which schedule (E or F) includes the parent item "
                  "(from EXPN_CD.G_FROM_E_F)",
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleGItem(Form460ScheduleGItemBase):
    """
    Payments made by on behalf of campaign filers.

    These transactions are itemized on Schedule G of the most recent version
    to each Form 460 filing. For payments itemized on any version of any Form
    460 filing, see Form460schedulegitemversion.

    Derived from EXPN_CD records where FORM_TYPE is 'G'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_g_items',
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
class Form460ScheduleGItemVersion(Form460ScheduleGItemBase):
    """
    Every version of the payments made on behalf of campaign filers.

    For payments itemized on Schedule G of the most recent version of each Form
    460 filing, see Form460ScheduleGitem.

    Derived from EXPN_CD records where FORM_TYPE is 'G'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_g_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the payment made'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


class Form460ScheduleIItemBase(CampaignContributionBase):
    """
    Abstract base model for items reported on Schedule I of Form 460 filings.

    On Schedule I, campaign filers are required to report miscellaneous cash
    increases during the period covered by the filing. These include any 
    transaction that increases the cash position of the filer, but is not a 
    monetary contribution, loan, or loan repayment.
    """
    amount = models.DecimalField(
        verbose_name='amount',
        decimal_places=2,
        max_digits=14,
        help_text="Amount of cash increase from the contributor in the period "
                  "covered by the filing (from RCPT_CD.AMOUNT)"
    )
    receipt_description = models.CharField(
        verbose_name='receipt description',
        max_length=90,
        blank=True,
        help_text="Description of the cash increase (from RCPT_CD.CTRIB_DSCR)"
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleIItem(Form460ScheduleIItemBase):
    """
    Miscellaneous cash increases to the coffers of campaign filers.

    Includes any transaction that increases the cash position of the filer, but
    is not a monetary contribution, loan, or loan repayment.

    These transactions are itemized on Schedule I of the most recent amendment
    to each Form 460 filing. For miscellaneous cash increases itemized on any
    version of any Form 460 filing, see Form460ScheduleIItemVersion.

    Derived from RCPT_CD records where FORM_TYPE is 'I'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_i_items',
        null=True,
        on_delete=models.SET_NULL,
        db_constraint=False,
        help_text='Foreign key referring to the Form 460 on which the '
                  'miscellaneous cash increase was report (from RCPT_CD.'
                  'FILING_ID)',
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
class Form460ScheduleIItemVersion(Form460ScheduleIItemBase):
    """
    Every version of the miscellaneous cash increases for campaign filers.

    Includes any transaction that increases the cash position of the filer, but
    is not a monetary contribution, loan, or loan repayment.

    For miscellaneous cash increases itemized on Schedule I of the most recent
    version of each Form 460 filing, see Form460ScheduleIItem.

    Derived from RCPT_CD records where FORM_TYPE is 'I'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_i_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the miscellaneous cash increase'
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_version',
            'line_item',
        ),)
        index_together = ((
            'filing_version',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )
