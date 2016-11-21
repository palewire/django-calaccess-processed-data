#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Abstract base models for campaign finance-related filings and transactions.
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


class CampaignContributionBase(models.Model):
    """
    Abstract base model for contributions received or made by campaign filers.

    These transactions are itemized on Schedules A, C and I of Form 460
    filings and stored in the RCPT_CD table.
    """
    line_item = models.IntegerField(
        verbose_name='line item',
        null=False,
        help_text='Line number of the filing form where the contribution is '
                  'itemized (from RCPT_CD.LINE_ITEM)',
    )
    date_received = models.DateField(
        verbose_name='date received',
        null=True,
        help_text='Date the contribution was received (from RCPT_CD.'
                  'RCPT_DATE)'
    )
    date_received_thru = models.DateField(
        verbose_name='date received thru',
        null=True,
        help_text='End date for late contributions received over a range of '
                  'days (from RCPT_CD.DATE_THRU)',
    )
    TRANSACTION_TYPE_CHOICES = (
        ('F', 'Forgiven Loan'),
        ('I', 'Intermediary'),
        ('R', 'Returned (Negative Amount?)'),
        ('T', 'Third Party Repayment'),
        ('X', 'Transfer'),
    )
    transaction_type = models.CharField(
        verbose_name='transaction type',
        max_length=1,
        choices=TRANSACTION_TYPE_CHOICES,
        help_text='Type of transaction (from RCPT_CD.TRAN_TYPE)',
    )
    transaction_id = models.CharField(
        verbose_name='transaction id',
        max_length=20,
        help_text='Identifies a unique transaction across versions of the a '
                  'given Form 460 filing (from RCPT_CD.TRAN_ID)'
    )
    memo_reference_number = models.CharField(
        verbose_name='memo reference number',
        max_length=20,
        blank=True,
        help_text='Reference number for the memo attached to the contribution '
                  '(from RCPT_CD.MEMO_REFNO)',
    )
    CONTRIBUTOR_CODE_CHOICES = (
        ('COM', 'Committee'),
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
        choices=CONTRIBUTOR_CODE_CHOICES,
        help_text='Code describing the contributor (from RCPT_CD.ENTITY_CD)',
    )
    contributor_committee_id = models.CharField(
        verbose_name='contributor committee id',
        max_length=9,
        blank=True,
        help_text="Contributor's filer identification number, if it is a "
                  "committee (from RCPT_CD.CMTE_ID)",
        )
    contributor_title = models.CharField(
        verbose_name='contributor title',
        max_length=10,
        blank=True,
        help_text='Name title of the contributor (from RCPT_CD.CTRIB_NAMT)',
    )
    contributor_lastname = models.CharField(
        verbose_name='contributor lastname',
        max_length=200,
        blank=True,
        help_text='Last name of the contributor or business name (from '
                  'RCPT_CD.CTRIB_NAML)',
    )
    contributor_firstname = models.CharField(
        verbose_name='contributor firstname',
        max_length=45,
        help_text='First name of the contributor (from RCPT_CD.CTRIB_NAMF)',
    )
    contributor_name_suffix = models.CharField(
        verbose_name='contributor name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the contributor (from RCPT_CD.CTRIB_NAMS)',
    )
    contributor_city = models.CharField(
        verbose_name='contributor city',
        max_length=30,
        blank=True,
        help_text='City of the contributor (from RCPT_CD.CTRIB_CITY)',
    )
    contributor_state = models.CharField(
        verbose_name='contributor state',
        max_length=2,
        blank=True,
        help_text='State of the contributor (from RCPT_CD.CTRIB_ST)',
    )
    contributor_zip = models.CharField(
        verbose_name='contributor zip',
        max_length=10,
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'contributor (from RCPT_CD.CTRIB_ZIP4)',
    )
    contributor_employer = models.CharField(
        verbose_name='contributor employer',
        max_length=200,
        blank=True,
        help_text='Employer of the contributor (from RCPT_CD.CTRIB_EMP)',
    )
    contributor_occupation = models.CharField(
        verbose_name='contributor occupation',
        max_length=60,
        blank=True,
        help_text='Occupation of the contributor (from RCPT_CD.CTRIB_OCC)',
    )
    contributor_is_self_employed = models.BooleanField(
        verbose_name='contributor is self employed',
        default=False,
        help_text='Indicates whether or not the contributor is self-employed'
                  '(from RCPT_CD.CTRIB_SELF)',
    )
    intermediary_committee_id = models.CharField(
        verbose_name='intermediary committee id',
        blank=True,
        max_length=9,
        help_text="Intermediary's filer identification number, if it is a "
                  "committee (from RCPT_CD.INTR_CMTEID)",
    ) 
    intermediary_title = models.CharField(
        verbose_name='intermediary title',
        max_length=10,
        blank=True,
        help_text='Name title of the intermediary (from RCPT_CD.INTR_NAMT)',
    )
    intermediary_lastname = models.CharField(
        verbose_name='intermediary lastname',
        max_length=200,
        blank=True,
        help_text='Last name of the intermediary or business name (from '
                  'RCPT_CD.INTR_NAML)',
    )
    intermediary_firstname = models.CharField(
        verbose_name='intermediary firstname',
        max_length=45,
        help_text='First name of the intermediary (from RCPT_CD.INTR_NAMF)',
    )
    intermediary_name_suffix = models.CharField(
        verbose_name='intermediary name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the intermediary (from RCPT_CD.INTR_NAMS)',
    )
    intermediary_city = models.CharField(
        verbose_name='intermediary city',
        max_length=30,
        blank=True,
        help_text='City of the intermediary (from RCPT_CD.INTR_CITY)',
    )
    intermediary_state = models.CharField(
        verbose_name='intermediary state',
        max_length=2,
        blank=True,
        help_text='State of the intermediary (from RCPT_CD.INTR_ST)',
    )
    intermediary_zip = models.CharField(
        verbose_name='intermediary zip',
        max_length=10,
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'intermediary (from RCPT_CD.INTR_ZIP4)',
    )
    intermediary_employer = models.CharField(
        verbose_name='intermediary employer',
        max_length=200,
        blank=True,
        help_text='Employer of the intermediary (from RCPT_CD.INTR_EMP)',
    )
    intermediary_occupation = models.CharField(
        verbose_name='intermediary occupation',
        max_length=60,
        blank=True,
        help_text='Occupation of the intermediary (from RCPT_CD.INTR_OCC)',
    )
    intermediary_is_self_employed = models.BooleanField(
        verbose_name='intermediary is self employed',
        default=False,
        help_text='(from S497_CD.INTR_SELF)',
    )
    cumulative_ytd_amount = models.DecimalField(
        decimal_places=2,
        max_digits=14,
        null=True,
        help_text="Cumulative year-to-date amount given by the contributor "
                  "as of the given Form 460 filing (from RCPT_CD.CUM_YTD)",
    )
    cumulative_election_amount = models.DecimalField(
        decimal_places=2,
        max_digits=14,
        null=True,
        help_text="For filers subject to contribution limits, cumulative "
                  "amount given by the contributor during the election "
                  "cycle as of the given Form 460 filing (from RCPT_CD."
                  "CUM_OTH)"
    )

    class Meta:
        abstract = True


class CampaignExpenditureItemBase(models.Model):
    """
    Abstract base model for payments made by or on behalf of campaign filers.

    These transactions are itemized on Schedules D, E and G of Form 460 filings
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
        verbose_name='payee committee id',
        max_length=9,
        blank=True,
        help_text="Payee's filer identification number, if it is a "
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
                  "EXPN_CD.EXPN_DSCR)",
    )
    amount = models.DecimalField(
        verbose_name='amount',
        decimal_places=2,
        max_digits=14,
        help_text="Amount paid to the payee in the period covered by the "
                  "filing (from EXPN_CD.AMOUNT)",
    )
    cumulative_ytd_amount = models.DecimalField(
        decimal_places=2,
        max_digits=14,
        null=True,
        help_text="Cumulative year-to-date amount given or spent by the filer "
                  "in support or opposition of the candidate or ballot "
                  "measure as of the Form 460's filing date (from EXPN_CD."
                  "CUM_YTD)",
    )
    expense_date = models.DateField(
        verbose_name="expense date",
        null=True,
        help_text="Date or expense (from EXPN_CD.EXPN_DATE)",
    )
    check_number = models.CharField(
        verbose_name='expense check number',
        max_length=20,
        blank=True,
        help_text="Optional check number for the payment made by the campaign "
                  "filer (from EXPN_CD.EXPN_CHKNO)",
    )
    SUPPORT_OPPOSE_CHOICES = (
        ('S', 'Support'),
        ('O', 'Oppose'),
        ('?', 'Unknown value')
    )
    support_oppose_code = models.CharField(
        verbose_name='support oppose code',
        max_length=1,
        blank=True,
        choices=SUPPORT_OPPOSE_CHOICES,
        help_text='If applicable, code indicating whether the payment went '
                  'toward supporting or opposing a candidate/ballot measure '
                  '(from EXPN_CD.SUP_OPP_CD)',  
    )
    ballot_measure_jurisdiction = models.CharField(
        verbose_name='ballot measure jurisdiction',
        max_length=40,
        blank=True,
        help_text="If the payment went toward supporting/opposing a ballot "
                  "measure, the jurisdiction subject to the ballot measure "
                  "(from EXPN_CD.BAL_JURIS)",
    )
    ballot_measure_name = models.CharField(
        verbose_name='ballot measure name', 
        max_length=200,
        blank=True,
        help_text="If the payment went toward supporting/opposing a ballot "
                  "measure, name of the ballot measure (from EXPN_CD.BAL_NAME "
                  " or EXPN_CD.CAND_NAML)"
    )
    ballot_measure_num = models.CharField(
        verbose_name='ballot measure number',
        max_length=7,
        blank=True,
        help_text="If the payment went toward supporting/opposing a ballot "
                  "measure, ballot number or letter (from EXPN_CD.BAL_NUM)",
    )
    candidate_title = models.CharField(
        verbose_name='candidate title',
        max_length=10,
        blank=True,
        help_text="If the payment went toward supporting/opposing a candidate,"
                  " name title of the candidate (from EXPN_CD.CAND_NAMT)",
    )
    candidate_lastname = models.CharField(
        verbose_name='candidate lastname',
        max_length=200,
        blank=True,
        help_text="If the payment went toward supporting/opposing a candidate,"
                  " last name of the candidate or business name (from EXPN_CD."
                  "CAND_NAML)",
    )
    candidate_firstname = models.CharField(
        verbose_name='candidate firstname',
        max_length=45,
        blank=True,
        help_text="If the payment went toward supporting/opposing a candidate,"
                  " first name of the candidate (from EXPN_CD.CAND_NAMF)",
    )
    candidate_name_suffix = models.CharField(
        verbose_name='candidate name suffix',
        max_length=10,
        blank=True,
        help_text="If the payment went toward supporting/opposing a candidate,"
                  " name suffix of the candidate (from EXPN_CD.CAND_NAMS)",
    )
    JURISDICTION_CODE_CHOICES = (
        ('ASM', 'Assembly District'),
        ('BOE', 'Board of Equalization District'),
        ('CIT', 'City'),
        ('CTY', 'County'),
        ('LOC', 'Local'),
        ('OTH', 'Other'),
        ('SEN', 'Senate District'),
        ('STW', 'Statewide'),
        ('???', 'Statewide'),
    )
    candidate_jurisdiction_code = models.CharField(
        verbose_name='candidate jurisdiction',
        max_length=3,
        blank=True,
        choices=JURISDICTION_CODE_CHOICES,
        help_text="If the payment went toward supporting/opposing a candidate,"
                  "code indicating the jurisdiction of the office (from"
                  " EXPN_CD.JURIS_CD)",
    )
    candidate_jurisdiction_description = models.CharField(
        verbose_name='candidate jurisdiciton description',
        max_length=40,
        blank=True,
        help_text="If the payment went toward supporting/opposing a county, "
                  "city or local candidate, full description of the office "
                  "(from EXPN_CD.JURIS_DSCR)",
    )
    candidate_district = models.CharField(
        verbose_name='candidate district',
        max_length=3,
        blank=True,
        help_text="If the payment went toward supporting/opposing a candidate,"
                  "for state senate, assembly or local board of education, the"
                  "district of the office (from EXPN_CD.DIST_NO)",
    )
    OFFICE_SOUGHT_HELD_CHOICES = (
        ('S', 'SOUGHT'),
        ('H', 'HELD'),
    )
    office_sought_held = models.CharField(
        verbose_name='office sought or held',
        max_length=1,
        blank=True,
        choices=OFFICE_SOUGHT_HELD_CHOICES,
        help_text="If the payment went toward supporting/opposing a candidate,"
                  "code indicating if the candidate is seeking or currently "
                  "holds the office (from EXPN_CD.OFF_S_H_CD)",
    )
    OFFICE_CODE_CHOICES = (
        ('APP', "State Appellate Court Justice"),
        ('ASM', 'State Assembly Person'),
        ('ASR', 'Assessor'),
        ('ATT', 'Attorney General'),
        ('BED', 'Board of Education'),
        ('BOE', 'Board of Equalization Member'),
        ('BSU', 'Board of Supervisors'),
        ('CAT', 'City Attorney'),
        ('CCB', 'Community College Board'),
        ('CCM', 'City Council Member'),
        ('CON', 'State Controller'),
        ('COU', 'County Counsel'),
        ('CSU', 'County Supervisor'),
        ('CTR', 'Local Controller'),
        ('DAT', 'District Attorney'),
        ('GOV', 'Governor'),
        ('INS', 'Insurance Commissioner'),
        ('LTG', 'Lieutenant Governor'),
        ('MAY', 'Mayor'),
        ('OTH', 'Other'),
        ('PDR', 'Public Defender'),
        ('PER', 'Public Employees Retirement System'),
        ('PLN', 'Planning Commissioner'),
        ('SCJ', 'Superior Court Judge'),
        ('SEN', 'State Senator'),
        ('SHC', 'Sheriff-Coroner'),
        ('SOS', 'Secretary of State'),
        ('SPM', 'Supreme Court Justice'),
        ('SUP', 'Superintendent of Public Instruction'),
        ('TRE', 'State Treasurer'),
        ('TRS', 'Local Treasurer'),
        ('???', 'Unknown value'),
    )
    office_code = models.CharField(
        verbose_name='office code',
        max_length=3,
        blank=True,
        choices=OFFICE_CODE_CHOICES,
        help_text="If the payment went toward supporting/opposing a candidate,"
                  "code describing the office (from EXPN_CD.OFFICE_CD)",
    )
    office_description = models.CharField(
        verbose_name='office description',
        max_length=40,
        blank=True,
        help_text="If the payment went toward supporting/opposing a candidate,"
                  "description of the office (from EXPN_CD.OFFIC_DSCR)",
    )
    transaction_id = models.CharField(
        verbose_name='transaction id',
        max_length=20,
        help_text='Identifies a unique transaction across versions of the a '
                  'given Form 460 filing (from EXPN_CD.TRAN_ID)',
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


class CampaignExpenditureSubItemBase(CampaignExpenditureItemBase):
    """
    Abstract base model for sub-items of campaign expenditures.

    A sub-item is a transaction where the amount is lumped into another
    "parent" payment reported elsewhere on the filing.
    """
    parent_transaction_id = models.CharField(
        verbose_name='parent transaction id',
        max_length=20,
        blank=True,
        help_text='Refers to a parent transaction itemized on the same Form '
                  '460 filing (from EXPN_CD.BAKREF_TID)',
    )

    class Meta:
        abstract = True


class CampaignLoanItemBase(models.Model):
    """
    Abstract base model for loans received or made by campaign filers.

    These transactions are itemized on Schedules B (Parts 1 and 2) and H of
    Form 460 filings and stored in the LOAN_CD table.
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
