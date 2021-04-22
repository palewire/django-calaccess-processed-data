#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Schedule 496, the Late Independent Expenditure Report.

More about the filing: https://calaccess.californiacivicdata.org/documentation/calaccess-forms/f496/
"""
from __future__ import unicode_literals

# Models
from django.db import models
from calaccess_processed_filings.models.campaign import CampaignFinanceFilingBase


class Form496Filing(CampaignFinanceFilingBase):
    """
    The most recent version of each Schedule 496 filing by campaign filers.

    Form 496 is filed by committees that make independent expenditures whose combined total is $1,000
    or more to support or oppose a single candidate for office or a single ballot measure.
    Form 496 should be filed within 24-hours of making the expenditure during the 90 days
    immediately preceding the election.

    Includes information from the cover sheet of the most recent amendment to
    each filing.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        primary_key=True,
        null=False,
        help_text='Unique identification number for the Schedule 496 filing ('
                  'from CVR_CAMPAIGN_DISCLOSURE_CD.FILING_ID)',
    )
    amendment_count = models.IntegerField(
        verbose_name='Count amendments',
        null=False,
        help_text='Number of amendments to the Schedule 496 filing (from '
                  'maximum value of CVR_CAMPAIGN_DISCLOSURE_CD.AMEND_ID)',
    )

    class Meta:
        """
        Model options.
        """
        app_label = 'calaccess_processed_filings'
        index_together = ((
            'filing_id',
            'amendment_count',
        ),)
        verbose_name = "Form 496 (Late Independent Expenditure) filing"

    def __str__(self):
        return str(self.filing_id)


class Form496FilingVersion(CampaignFinanceFilingBase):
    """
    Every version of each Schedule 496 filing by a campaign filer.

    Includes information found on the cover sheet of each version of each
    Schedule 496 filing.
    """
    filing = models.ForeignKey(
        'Form496Filing',
        related_name='versions',
        db_constraint=False,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Unique identification number for the Schedule 496 filing ('
                  'from S496_CD.FILING_ID)',
    )
    amend_id = models.IntegerField(
        null=False,
        help_text='Identifies the version of the Schedule 496 filing, with 0 '
                  'representing the initial filing (from CVR_CAMPAIGN_'
                  'DISCLOSURE_CD.AMEND_ID)',
    )

    class Meta:
        """
        Model options.
        """
        app_label = 'calaccess_processed_filings'
        unique_together = ((
            'filing',
            'amend_id',
        ),)
        index_together = ((
            'filing',
            'amend_id',
        ),)
        verbose_name = "Form 496 (Late Independent Expenditure) filing version"

    def __str__(self):
        return '%s-%s' % (self.filing, self.amend_id)
