#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Schedule 497, the Late Contribution Reports.

More about the filing: http://calaccess.californiacivicdata.org/documentation/calaccess-forms/f497/
"""
# Models
from django.db import models
from calaccess_processed_filings.models.campaign import CampaignFinanceFilingBase


class Form497Filing(CampaignFinanceFilingBase):
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
        app_label = 'calaccess_processed_filings'
        index_together = ((
            'filing_id',
            'amendment_count',
        ),)
        verbose_name = "Form 497 (Late Contribution) filing"

    def __str__(self):
        return str(self.filing_id)


class Form497FilingVersion(CampaignFinanceFilingBase):
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
        app_label = 'calaccess_processed_filings'
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
