#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing Part 1 data from Schedule 497, the Late Independent Expenditure Reports.

More about the filing: https://calaccess.californiacivicdata.org/documentation/calaccess-forms/f496/
"""
from django.db import models
from calaccess_processed_filings.models.base import FilingBaseModel


class Form496Part1ItemBase(FilingBaseModel):
    """
    Abstract base model for items reported on Part 1 of Schedule 496 filings.

    On Part 1 of Schedule 496, campaign filers are required to report the candidates or ballot measure
    they are supported or opposing with their independent expenditures.
    """
    candidate_title = models.CharField(
        verbose_name='candidate title',
        max_length=10,
        blank=True,
        help_text='Name title of the candidate (from CVR_CAMPAIGN_DISCLOSURE_CD.CAND_NAMT)',
    )
    candidate_lastname = models.CharField(
        verbose_name='candidate lastname',
        max_length=200,
        blank=True,
        help_text='Last name of the candidate (from CVR_CAMPAIGN_DISCLOSURE_CD.CAND_NAML)',
    )
    candidate_firstname = models.CharField(
        verbose_name='candidate firstname',
        max_length=45,
        help_text='First name of the candidate (from CVR_CAMPAIGN_DISCLOSURE_CD.CAND_NAMF)',
    )
    candidate_name_suffix = models.CharField(
        verbose_name='candidate name suffix',
        max_length=10,
        blank=True,
        help_text='Name suffix of the candidate (from CVR_CAMPAIGN_DISCLOSURE_CD.CAND_NAMS)',
    )
    candidate_id = models.CharField(
        verbose_name='candidate id',
        max_length=9,
        blank=True,
        help_text='Identifies the candidate to whom the contribution is '
                  'connected (from S497_CD.CAND_ID). This can be translated '
                  'to the filer_id by joining to FILER_XREF_CD.',
    )
    candidate_office_code = models.CharField(
        verbose_name='candidate office code',
        max_length=3,
        blank=True,
        help_text='Code describing the office sought sought by the candidate '
                  '(from CVR_CAMPAIGN_DISCLOSURE_CD.OFFICE_CD)',
    )
    ballot_measure_name = models.CharField(
        verbose_name='Ballot measure name',
        max_length=200,
        blank=True,
        help_text='Name of the ballot measure supported or opposed by the '
                  'recipient (from CVR_CAMPAIGN_DISCLOSURE_CD.BAL_NAME)',
    )
    ballot_measure_number = models.CharField(
        verbose_name='Ballot measure number',
        max_length=7,
        blank=True,
        help_text='Ballot measure number (from CVR_CAMPAIGN_DISCLOSURE_CD.BAL_NUM)',
    )
    ballot_measure_jurisdiction = models.CharField(
        verbose_name='ballot measure jurisdiction',
        max_length=40,
        blank=True,
        help_text='Jurisdiction of the ballot measure supported or opposed by '
                  'the recipient (from CVR_CAMPAIGN_DISCLOSURE_CD.BAL_JURIS)',
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
                  'the candidate or ballot measure (from CVR_CAMPAIGN_DISCLOSURE_CD.SUP_OPP_CD)',
    )

    class Meta:
        """
        Model options.
        """
        app_label = 'calaccess_processed_filings'
        abstract = True


class Form496Part1Item(Form496Part1ItemBase):
    """
    Late independent expenditures made by campaign filers.

    These transactions are itemized on Part 1 of the most recent version
    of each Schedule 496 filing.
    """
    filing = models.ForeignKey(
        'Form496Filing',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Unique identification number for the Schedule 496 filing (from S496_CD.FILING_ID)',
    )

    class Meta:
        """
        Model options.
        """
        app_label = 'calaccess_processed_filings'
        verbose_name = "Form 496 (Late Independent Expenditure) Part 1 item"

    def __str__(self):
        return str(self.filing)


class Form496Part1ItemVersion(Form496Part1ItemBase):
    """
    Every version of each late independent expenditures made by campaign filers.
    """
    filing_version = models.ForeignKey(
        'Form496FilingVersion',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Schedule 496 that includes the received contribution'
    )

    class Meta:
        """
        Model options.
        """
        app_label = 'calaccess_processed_filings'
        verbose_name = "Form 496 (Late Independent Expenditure) Part 1 item version"

    def __str__(self):
        return '%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id
        )
