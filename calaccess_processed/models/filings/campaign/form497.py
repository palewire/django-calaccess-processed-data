#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Schedule 497, the Late Contribution Reports.

More about the filing: http://calaccess.californiacivicdata.org/documentation/calaccess-forms/f497/
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.filings import (
    FilingMixin,
    FilingVersionMixin,
)
from calaccess_processed.models.base import CalAccessBaseModel
from calaccess_processed.models.filings.campaign import CampaignFinanceFilingBase


@python_2_unicode_compatible
class Form497Filing(FilingMixin, CampaignFinanceFilingBase):
    """
    The most recent version of each Schedule 497 filing by campaign filers.

    Form 497 is the Late Contribution Report filed by state and local committees
    making or receiving contributions totaling $1,000 or more in the 90 days
    before an election, committees reporting contributions of $5,000 or more in
    connection with a state ballot measure and state candidates as well as state
    ballot measure committees that receive $5,000 or more at any time other than
    a 90-day election cycle.

    Includes information from the cover sheet of the most recent amendment to
    each filing. All versions of Schedule 497 filings can be found in
    schedule497version.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        primary_key=True,
        null=False,
        help_text='Unique identification number for the Schedule 497 filing ('
                  'from CVR_CAMPAIGN_DISCLOSURE_CD.FILING_ID)',
    )
    amendment_count = models.IntegerField(
        verbose_name='Count amendments',
        null=False,
        help_text='Number of amendments to the Schedule 497 filing (from '
                  'maximum value of CVR_CAMPAIGN_DISCLOSURE_CD.AMEND_ID)',
    )

    class Meta:
        """
        Model options.
        """
        index_together = ((
            'filing_id',
            'amendment_count',
        ),)
        verbose_name = "Form 497 (Late Contribution) filing"

    def __str__(self):
        return str(self.filing_id)


@python_2_unicode_compatible
class Form497FilingVersion(FilingVersionMixin, CampaignFinanceFilingBase):
    """
    Every version of each Schedule 497 filing by a campaign filer.

    Includes information found on the cover sheet of each version of each
    Schedule 497 filing. For the most recent version of each filing, see
    schedule497filing.
    """
    filing = models.ForeignKey(
        'Form497Filing',
        related_name='versions',
        db_constraint=False,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Unique identification number for the Schedule 497 filing ('
                  'from S497_CD.FILING_ID)',
    )
    amend_id = models.IntegerField(
        null=False,
        help_text='Identifies the version of the Schedule 497 filing, with 0 '
                  'representing the initial filing (from CVR_CAMPAIGN_'
                  'DISCLOSURE_CD.AMEND_ID)',
    )

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing',
            'amend_id',
        ),)
        index_together = ((
            'filing',
            'amend_id',
        ),)
        verbose_name = "Form 497 (Late Contribution) filing version"

    def __str__(self):
        return '%s-%s' % (self.filing, self.amend_id)


class Form497ItemBase(CalAccessBaseModel):
    """
    Abstract base model for items reported on Schedule 497 filings.

    On Schedule 497, campaign filers are required to report late contributions
    received or made in the 90 days leading up to an election.
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
        abstract = True


class Form497Part1ItemBase(Form497ItemBase):
    """
    Abstract base model for items reported on Part 1 of Schedule 497 filings.

    On Part 1 of Schedule 497, campaign filers are required to report
    contributions received in the 90 days leading up to an election.
    """
    CONTRIBUTOR_CODE_CHOICES = (
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
        choices=CONTRIBUTOR_CODE_CHOICES,
        help_text='Code describing the contributor (from S497_CD.ENTITY_CD)',
    )
    contributor_committee_id = models.CharField(
        verbose_name='committee id',
        max_length=9,
        blank=True,
        help_text="Contributor's filer identification number, if it is a "
                  "committee (from RCPT_CD.CMTE_ID)",
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
        help_text='Indicates whether or not the contributor is self-employed'
                  '(from S497_CD.CTRIB_SELF)',
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class Form497Part1Item(Form497Part1ItemBase):
    """
    Late contributions received by campaign filers.

    These transactions are itemized on Part 1 of the most recent version
    of each Schedule 497 filing. For receipts of late contributions itemized
    on any version of any Schedule 497 filing, see Form497Part1ItemVersion.

    Derived from S497_CD records where FORM_TYPE is 'F497P1'.
    """
    filing = models.ForeignKey(
        'Form497Filing',
        related_name='contributions_received',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Unique identification number for the Schedule 497 filing ('
                  'from S497_CD.FILING_ID)',
    )

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing',
            'line_item',
        ),)
        verbose_name = "Form 497 (Late Contribution) Part 1 item"

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form497Part1ItemVersion(Form497Part1ItemBase):
    """
    Every version of each late contribution received by a campaign filer.

    For late contributions itemized on Part 1 of the most recent version of
    each Schedule 497 filing, see Form497Part1Item.

    Derived from S497_CD records where FORM_TYPE is 'F497P1'.
    """
    filing_version = models.ForeignKey(
        'Form497FilingVersion',
        related_name='contributions_received',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Schedule 497 '
                  'that includes the received contribution'
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
        verbose_name = "Form 497 (Late Contribution) Part 1 item version"

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


class Form497Part2ItemBase(Form497ItemBase):
    """
    Abstract base model for items reported on Part 2 of Schedule 497 filings.

    On Part 2 of Schedule 497, campaign filers are required to report
    contributions made in the 90 days leading up to an election.
    """
    RECIPIENT_CODE_CHOICES = (
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
        choices=RECIPIENT_CODE_CHOICES,
        help_text='Code describing the recipient (from S497_CD.ENTITY_CD)',
    )
    recipient_committee_id = models.CharField(
        verbose_name='recipient committee id',
        max_length=9,
        blank=True,
        help_text='Filer identification number identifying the recipient if it '
                  'is a committee (from S497_CD.CMTE_ID)'
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
        help_text='Identifies the candidate to whom the contribution is '
                  'connected (from S497_CD.CAND_ID). This can be translated '
                  'to the filer_id by joining to FILER_XREF_CD.',
    )
    candidate_title = models.CharField(
        verbose_name='candidate title',
        max_length=10,
        blank=True,
        help_text='Name title of the candidate to whom the contribution is '
                  'connected (from S497_CD.CAND_NAMT)',
    )
    candidate_lastname = models.CharField(
        verbose_name='candidate last name',
        max_length=200,
        blank=True,
        help_text='Last name of the candidate to whom the contribution is '
                  'connected (S497_CD.CAND_NAML)',
    )
    candidate_firstname = models.CharField(
        verbose_name='candidate first name',
        max_length=45,
        blank=True,
        help_text='First name of the candidate to whom the contribution is '
                  'connected (S497_CD.CAND_NAMF)',
    )
    candidate_namesuffix = models.CharField(
        verbose_name='candidate name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the candidate to whom the contribution is '
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
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class Form497Part2Item(Form497Part2ItemBase):
    """
    Late contributions made by campaign filers.

    These transactions are itemized on Part 2 of the most recent version
    of each Schedule 497 filing. For gifts of late contributions itemized on
    any version of any Schedule 497 filing, see Form497Part2ItemVersion.

    Derived from S497_CD records where FORM_TYPE is 'F497P2'.
    """
    filing = models.ForeignKey(
        'Form497Filing',
        related_name='contributions_made',
        db_constraint=False,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Unique identification number for the Schedule 497 filing ('
                  'from S497_CD.FILING_ID)',
    )

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing',
            'line_item',
        ),)
        verbose_name = "Form 497 (Late Contribution) Part 2 item"

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form497Part2ItemVersion(Form497Part2ItemBase):
    """
    Every version of each late contribution made by a campaign filer.

    For late contributions itemized on Part 2 of the most recent version of
    each Schedule 497 filing, see Form497Part2Item.

    Derived from S497_CD records where FORM_TYPE is 'F497P2'.
    """
    filing_version = models.ForeignKey(
        'Form497FilingVersion',
        related_name='contributions_made',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Schedule 497 '
                  'that includes the given contribution'
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
        verbose_name = "Form 497 (Late Contribution) Part 2 item version"

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )
