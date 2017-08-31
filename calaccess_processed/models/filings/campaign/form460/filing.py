#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Campaign Disclosure Statements (Form 460).
"""
from __future__ import unicode_literals
from django.db import models
from .base import Form460FilingBase
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.filings import (
    FilingMixin,
    FilingVersionMixin,
)


@python_2_unicode_compatible
class Form460Filing(FilingMixin, Form460FilingBase):
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

    class Meta:
        """
        Model options.
        """
        index_together = ((
            'filing_id',
            'amendment_count',
        ),)
        verbose_name = "Form 460 (Campaign Disclosure) filing"

    def __str__(self):
        return str(self.filing_id)


@python_2_unicode_compatible
class Form460FilingVersion(FilingVersionMixin, Form460FilingBase):
    """
    Every version of each Form 460 (Campaign Disclosure Statement) filing by recipient committees.

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
        verbose_name = "Form 460 (Campaign Disclosure) filing version"

    def __str__(self):
        return '%s-%s' % (self.filing, self.amend_id)
