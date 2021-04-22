#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Schedule 497, the Late Contribution Reports.

More about the filing: http://calaccess.californiacivicdata.org/documentation/calaccess-forms/f497/
"""
from django.db import models
from .base import Form497ItemBase


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
        app_label = 'calaccess_processed_filings'
        abstract = True


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
        app_label = 'calaccess_processed_filings'
        unique_together = ((
            'filing',
            'line_item',
        ),)
        verbose_name = "Form 497 (Late Contribution) Part 1 item"

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


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
        app_label = 'calaccess_processed_filings'
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
