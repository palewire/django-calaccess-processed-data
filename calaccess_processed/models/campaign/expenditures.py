#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing campaign-related transactions derived from raw CAL-ACCESS data.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.managers import ProcessedDataManager


class CampaignExpenditureBase(models.Model):
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
                  "name title of the candidate (from EXPN_CD.CAND_NAMT)",
    )
    candidate_lastname = models.CharField(
        verbose_name='candidate lastname',
        max_length=200,
        blank=True,
        help_text="If the payment went toward supporting/opposing a candidate,"
                  "last name of the candidate or business name (from EXPN_CD."
                  "CAND_NAML)",
    )
    candidate_firstname = models.CharField(
        verbose_name='candidate firstname',
        max_length=45,
        blank=True,
        help_text="If the payment went toward supporting/opposing a candidate,"
                  "first name of the candidate (from EXPN_CD.CAND_NAMF)",
    )
    candidate_name_suffix = models.CharField(
        verbose_name='candidate name suffix',
        max_length=10,
        blank=True,
        help_text="If the payment went toward supporting/opposing a candidate,"
                  "Name suffix of the candidate (from EXPN_CD.CAND_NAMS)",
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


class CampaignExpenditureSubItemBase(CampaignExpenditureBase):
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


class ScheduleDItemBase(CampaignExpenditureBase):
    """
    Abstract base model for items reported on Schedule D of Form 460.

    On Schedule D, campaign filers are required to summarize contributions
    and independent expenditures in support or opposition to other candidates
    and ballot measures
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
class ScheduleDItem(ScheduleDItemBase):
    """
    Contribution and expenditures in support or opposition to other candidates
    and ballot measures.

    These transactions are itemized on Schedule D of the most recent version
    to each Form 460 filing. For payments itemized on any version of any Form
    460 filing, see scheduleditemversion.

    Derived from EXPN_CD records where FORM_TYPE is 'D'.
    """
    filing = models.ForeignKey(
        'Form460',
        related_name='schedule_d_items',
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
class ScheduleDItemVersion(ScheduleDItemBase):
    """
    Every version of the payments made on behalf of campaign filers.

    For payments itemized on Schedule D of the most recent version of each Form
    460 filing, see scheduleditem.

    Derived from EXPN_CD records where FORM_TYPE is 'D'.
    """
    filing_version = models.ForeignKey(
        'Form460Version',
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
class ScheduleEItem(CampaignExpenditureBase):
    """
    Payments made by campaign filers, itemized on Schedule E of Form 460.

    These transactions are itemized on the most recent version of each Form 460
    filing. For payments itemized on any version of any Form 460 filing, see
    scheduleeitemversion.

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
        'Form460',
        related_name='schedule_e_items',
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
class ScheduleEItemVersion(CampaignExpenditureBase):
    """
    Every version of the payments made, itemized on Form 460 Schedule E.

    For payments itemized on the most recent version of each Form 460 filing,
    see scheduleeitem.

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
        'Form460Version',
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
class ScheduleESubItem(CampaignExpenditureSubItemBase):
    """
    Sub-items of payments made by campaign filers.

    These transactions are itemized on Schedule E of the most recent version
    of each Form 460 filing. For payments sub-itemitemized on any version of
    any Form 460 filing, see scheduleesubitemversion.

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
        'Form460',
        related_name='schedule_e_subitems',
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
class ScheduleESubItemVersion(CampaignExpenditureSubItemBase):
    """
    Every version of the sub-items of payments by campaign filers.

    For payments sub-itemized on Schedule E of the most recent version of each
    Form 460 filing, see scheduleesubitem.

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
        'Form460Version',
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


class ScheduleGItemBase(CampaignExpenditureSubItemBase):
    """
    Abstract base model for items reported on Schedule G of Form 460.
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
class ScheduleGItem(ScheduleGItemBase):
    """
    Payments made by on behalf of campaign filers.

    These transactions are itemized on Schedule G of the most recent version
    to each Form 460 filing. For payments itemized on any version of any Form
    460 filing, see schedulegitemversion.

    Derived from EXPN_CD records where FORM_TYPE is 'G'.
    """
    filing = models.ForeignKey(
        'Form460',
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
class ScheduleGItemVersion(ScheduleGItemBase):
    """
    Every version of the payments made on behalf of campaign filers.

    For payments itemized on Schedule G of the most recent version of each Form
    460 filing, see schedulegitem.

    Derived from EXPN_CD records where FORM_TYPE is 'G'.
    """
    filing_version = models.ForeignKey(
        'Form460Version',
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
