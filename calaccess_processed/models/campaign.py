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

    objects = ProcessedDataManager()

    class Meta:
        """
        Meta model options.
        """
        app_label = 'calaccess_processed'

    def __str__(self):
        return str(self.full_name)


@python_2_unicode_compatible
class CandidateCommittee(models.Model):
    """
    Maps links between candidates and recipient committees.

    Derived from FILER_LINKS_CD.
    """
    candidate_filer_id = models.IntegerField(
        verbose_name='candidate filer ID',
        null=False,
        help_text="Unique filer_id of the candidate. Derived from FILER_ID_A "
                  "and FILER_ID_B columns on FILER_LINKS_CD, includes any "
                  "filer_id ever categorized as a candidate in "
                  "FILER_TO_FILER_TYPES_CD.",
    )
    committee_filer_id = models.IntegerField(
        verbose_name='committee filer ID',
        null=False,
        help_text="Unique filer_id of the committee linked to the candidate. "
                  "Derived from FILER_ID_A and FILER_ID_B columns on "
                  "FILER_LINKS_CD, includes any filer_id ever categorized as a"
                  " recipient committee that is linked to a filer_id "
                  "categorized as a candidate in FILER_TO_FILER_TYPES_CD.",
    )
    link_type_id = models.IntegerField(
        verbose_name='link type identifier',
        null=False,
        help_text="Numeric identifier that describes how the candidate and "
                  "committee are linked (the absolute value of FILER_LINKS_CD."
                  "LINK_TYPE).",
    )
    link_type_description = models.CharField(
        verbose_name='link type description',
        max_length=100,
        blank=False,
        null=False,
        help_text="Human-readable description of the link between the candidate"
                  " and committee (from LOOKUP_CODES_CD.CODE_DESC).",
    )
    first_session = models.IntegerField(
        verbose_name='first session',
        null=True,
        help_text="First session when the link between the candidate and "
                  "commitee existed (minimum value of "
                  "FILER_LINKS_CD.SESSION_ID).",
    )
    last_session = models.IntegerField(
        verbose_name='last session',
        null=True,
        help_text="Last session when the link between the candidate and "
                  "commitee existed (maximum value of "
                  "FILER_LINKS_CD.SESSION_ID).",
    )
    first_effective_date = models.DateField(
        verbose_name='first effective date',
        null=False,
        help_text="Earliest date when the link between the candidate and "
                  "commitee was in effect (minimum value of "
                  "FILER_LINKS_CD.EFFECTIVE_DATE).",
    )
    last_effective_date = models.DateField(
        verbose_name='last effective date',
        null=False,
        help_text="Latest date when the link between the candidate and "
                  "commitee was in effect (maximum value of "
                  "FILER_LINKS_CD.EFFECTIVE_DATE).",
    )
    first_termination_date = models.DateField(
        verbose_name='first termination date',
        null=True,
        help_text="Earliest date when the link between the candidate and "
                  "commitee was terminated (minimum value of "
                  "FILER_LINKS_CD.TERMINATION_DATE).",
    )
    last_termination_date = models.DateField(
        verbose_name='last termination date',
        null=True,
        help_text="Latest date when the link between the candidate and "
                  "commitee was terminated (minimum value of "
                  "FILER_LINKS_CD.TERMINATION_DATE).",
    )

    objects = ProcessedDataManager()

    class Meta:
        """
        Meta model options.
        """
        app_label = 'calaccess_processed'
        unique_together = ((
            'candidate_filer_id',
            'committee_filer_id',
            'link_type_id'
        ),)

    def __str__(self):
        return str(self.committee_filer_id)


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


class LateContributionBase(models.Model):
    """
    Abstract base model for late contributions received or made.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        db_index=True,
        null=False,
        help_text='Unique identification number for the Schedule 497 filing ('
                  'from S497_CD.FILING_ID)',
    )
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
        abstract = True


class LateContributionReceivedBase(LateContributionBase):
    """
    Abstract base model for late contributions received.
    """
    CONTRIBUTOR_CD_CHOICES = (
        ('BNM', 'Ballot measure name/title'),
        ('CAO', 'Candidate/officeholder'),
        ('COM', 'Committee'),
        ('CTL', 'Controlled committee'),
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
        choices=CONTRIBUTOR_CD_CHOICES,
        help_text='Code describing the contributor (from S497_CD.ENTITY_CD)',
    )
    contributor_title = models.CharField(
        verbose_name='contributor title',
        max_length=10,
        blank=True,
        help_text='Name title of the contributor (from S497_CD.ENTY_NAMT)',
    )
    contributor_lastname = models.CharField(
        verbose_name='contributor lastname',
        max_length=200,
        blank=True,
        help_text='Last name of the contributor (from S497_CD.ENTY_NAML)',
    )
    contributor_firstname = models.CharField(
        verbose_name='contributor firstname',
        max_length=45,
        help_text='First name of the contributor (from S497_CD.ENTY_NAMF)',
    )
    contributor_name_suffix = models.CharField(
        verbose_name='contributor name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the contributor (from S497_CD.ENTY_NAMS)',
    )
    contributor_city = models.CharField(
        verbose_name='contributor city',
        max_length=30,
        blank=True,
        help_text='City of the contributor (from S497_CD.ENTY_CITY)',
    )
    contributor_state = models.CharField(
        verbose_name='contributor state',
        max_length=2,
        blank=True,
        help_text='State of the contributor (from S497_CD.ENTY_ST)',
    )
    contributor_zip = models.CharField(
        verbose_name='contributor zip',
        max_length=10,
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'contributor (from S497_CD.ENTY_ZIP4)',
    )
    contributor_employer = models.CharField(
        verbose_name='contributor employer',
        max_length=200,
        blank=True,
        help_text='Employer of the contributor (from S497_CD.CTRIB_EMP)',
    )
    contributor_occupation = models.CharField(
        verbose_name='contributor occupation',
        max_length=60,
        blank=True,
        help_text='Occupation of the contributor (from S497_CD.CTRIB_OCC)',
    )
    contributor_is_self_employed = models.BooleanField(
        verbose_name='contributor is self employed',
        default=False,
        help_text='(from S497_CD.CTRIB_SELF)',
    )
    committee_id = models.CharField(
        verbose_name='committee id',
        max_length=9,
        db_index=True,
        blank=True,
        help_text='Filer identification number identifying the contributor '
                  '(from S497_CD.CMTE_ID)',
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class LateContributionReceived(LateContributionReceivedBase):
    """
    Late contributions received, as itemized on Part 1 of Schedule 497 filings.

    Includes transactions itemized on the most recent amendment to the given
    Schedule 497 filing. For transactions itemized on any version of a 
    Schedule 497 filing, see latecontributionreceivedversion.

    Derived from S497_CD records where FORM_TYPE is 'F497P1'.
    """
    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_id',
            'line_item',
        ),)
        verbose_name_plural = 'Late contributions received'

    def __str__(self):
        return str(self.filing_id)


@python_2_unicode_compatible
class LateContributionReceivedVersion(LateContributionReceivedBase):
    """
    Every version of a late contribution received transaction, as itemized on 
    Part 1 of each version of each Schedule 497 filings.

    For contributions itemized on the most recent version of the Schedule 497 
    filing, see latecontributionreceived.

    Derived from S497_CD records where FORM_TYPE is 'F497P1'.
    """
    amend_id = models.IntegerField(
        verbose_name='amendment id',
        db_index=True,
        null=False,
        help_text='Identifies the version of the Schedule 497 filing, with 0 '
                  'representing the initial filing (from S497_CD.AMEND_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_id',
            'amend_id',
            'line_item',
        ),)

    def __str__(self):
        return str(self.filing_id)


class LateContributionMadeBase(LateContributionBase):
    """
    Abstract base model for late contributions received.
    """
    RECIPIENT_CD_CHOICES = (
        ('BNM', 'Ballot measure name/title'),
        ('CAO', 'Candidate/officeholder'),
        ('COM', 'Committee'),
        ('CTL', 'Controlled committee'),
        ('IND', 'Individual'),
        ('OTH', 'Other'),
        ('PTY', 'Political Party'),
        ('RCP', 'Recipient committee'),
        ('SCC', 'Small Contributor Committee'),
    )
    recipient_code = models.CharField(
        verbose_name='recipient code',
        max_length=3,
        blank=True,
        choices=RECIPIENT_CD_CHOICES,
        help_text='Code describing the recipient (from S497_CD.ENTITY_CD)',
    )
    recipient_committee_id = models.CharField(
            verbose_name='recipient committee id',
            max_length=9,
            db_index=True,
            blank=True,
            help_text='Filer identification number identifying the recipient if it'
                      'is a committee (from S497_CD.CMTE_ID)',
        )
    recipient_title = models.CharField(
        verbose_name='recipient title',
        max_length=10,
        blank=True,
        help_text='Name title of the recipient (from S497_CD.ENTY_NAMT)',
    )
    recipient_lastname = models.CharField(
        verbose_name='recipient lastname',
        max_length=200,
        blank=True,
        help_text='Last name of the recipient (from S497_CD.ENTY_NAML)',
    )
    recipient_firstname = models.CharField(
        verbose_name='recipient firstname',
        max_length=45,
        help_text='First name of the recipient (from S497_CD.ENTY_NAMF)',
    )
    recipient_name_suffix = models.CharField(
        verbose_name='recipient name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the recipient (from S497_CD.ENTY_NAMS)',
    )
    recipient_city = models.CharField(
        verbose_name='recipient city',
        max_length=30,
        blank=True,
        help_text='City of the recipient (from S497_CD.ENTY_CITY)',
    )
    recipient_state = models.CharField(
        verbose_name='recipient state',
        max_length=2,
        blank=True,
        help_text='State of the recipient (from S497_CD.ENTY_ST)',
    )
    recipient_zip = models.CharField(
        verbose_name='recipient zip',
        max_length=10,
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'recipient (from S497_CD.ENTY_ZIP4)',
    )
    candidate_id = models.CharField(
        verbose_name='candidate id',
        max_length=9,
        blank=True,
        help_text = 'Identifies the candidate to whom the contribution is '
                    'connected (from S497_CD.CAND_ID). This can be translated '
                    'to the filer_id by joining to FILER_XREF_CD.',
    )
    candidate_title = models.CharField(
        verbose_name='candidate title',
        max_length=10,
        blank=True,
        help_text = 'Name title of the candidate to whom the contribution is '
                    'connected (from S497_CD.CAND_NAMT)',
    )
    candidate_lastname = models.CharField(
        verbose_name='candidate last name',
        max_length=200,
        blank=True,
        help_text = 'Last name of the candidate to whom the contribution is '
                    'connected (S497_CD.CAND_NAML)',
    )
    candidate_firstname = models.CharField(
        verbose_name='candidate first name',
        max_length=45,
        blank=True,
        help_text = 'First name of the candidate to whom the contribution is '
                    'connected (S497_CD.CAND_NAMF)',
    )
    candidate_namesuffix = models.CharField(
        verbose_name='candidate name suffix',
        max_length=10,
        blank=True,
        help_text = 'Name suffix of the candidate to whom the contribution is '
                    'connected (S497_CD.CAND_NAMS)',
    )
    candidate_office_code = models.CharField(
        verbose_name='candidate office code',
        max_length=3,
        blank=True,
        help_text='Code describing the office sought sought by the candidate '
                  '(from S497_CD.OFFICE_CD)',
    )
    candidate_office_description = models.CharField(
        verbose_name='candidate office description',
        max_length=40,
        blank=True,
        help_text='Full description of the office sought by the candidate '
                  '(from S497_CD.OFFIC_DSCR)',
    )
    candidate_jurisdiction_code = models.CharField(
        verbose_name='candidate jursidiction code',
        max_length=3,
        blank=True,
        help_text='Code describing the jurisdiction of office sought by the '
                  'candidate (from S497_CD.JURIS_CD)',
    )
    candidate_jurisdiction_description = models.CharField(
        verbose_name='candidate jurisdiction description',
        max_length=40,
        blank=True,
        help_text='Full description of the jurisdiction of the office sought '
                  'by the candidate (from S497_CD.JURIS_DSCR)',
    )
    candidate_district = models.CharField(
        verbose_name='candidate district',
        max_length=3,
        blank=True,
        help_text='District of the office sought by the candidate (from '
                  'S497_CD.DIST_NO)',
    )
    ballot_measure_name = models.CharField(
        verbose_name='Ballot measure name',
        max_length=200,
        blank=True,
        help_text='Name of the ballot measure supported or opposed by the '
                  'recipient (from S497_CD.BAL_NAME)',
    )
    ballot_measure_number = models.CharField(
        verbose_name='Ballot measure number',
        max_length=7,
        blank=True,
        help_text='Ballot measure number (from S497_CD.BAL_NUM)',
    )
    ballot_measure_jurisdiction = models.CharField(
        verbose_name='ballot measure jurisdiction',
        max_length=40,
        blank=True,
        help_text='Jurisdiction of the ballot measure supported or opposed by '
                  'the recipient (from S497_CD.BAL_JURIS)',
    )
    SUPPORT_OPPOSITION_CODE_CHOICES = (
        ('O', 'Opposition'),
        ('S', 'Support'),
    )
    support_opposition_code = models.CharField(
        verbose_name='support opposition code',
        max_length=1,
        choices=SUPPORT_OPPOSITION_CODE_CHOICES,
        blank=True,
        help_text='Code describing whether the contribuitor supports or opposes'
                  'the candidate or ballot measure (from S497_CD.SUP_OPP_CD)',
    )
    election_date = models.DateField(
        verbose_name='election date',
        null=True,
        help_text='Date of the election (from S497_CD.ELEC_DATE)',
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class LateContributionMade(LateContributionMadeBase):
    """
    Late contributions made, as itemized on Part 2 of Schedule 497 filings.

    Includes transactions itemized on the most recent amendment to the given
    Schedule 497 filing. For transactions itemized on any version of a 
    Schedule 497 filing, see latecontributionmadeversion.

    Derived from S497_CD records where FORM_TYPE is 'F497P2'.
    """
    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_id',
            'line_item',
        ),)
        verbose_name_plural = 'Late contributions made'

    def __str__(self):
        return str(self.filing_id)


@python_2_unicode_compatible
class LateContributionMadeVersion(LateContributionMadeBase):
    """
    Every version of a late contribution made transaction, as itemized on 
    Part 2 of each version of each Schedule 497 filings.

    For contributions itemized on the most recent version of the Schedule 497 
    filing, see latecontributionmade.

    Derived from S497_CD records where FORM_TYPE is 'F497P2'.
    """
    amend_id = models.IntegerField(
        verbose_name='amendment id',
        db_index=True,
        null=False,
        help_text='Identifies the version of the Schedule 497 filing, with 0 '
                  'representing the initial filing (from S497_CD.AMEND_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        unique_together = ((
            'filing_id',
            'amend_id',
            'line_item',
        ),)

    def __str__(self):
        return str(self.filing_id)
