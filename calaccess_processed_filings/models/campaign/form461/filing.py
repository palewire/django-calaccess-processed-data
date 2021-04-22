#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Campaign Disclosure Statements (Form 461).
"""
from django.db import models
from calaccess_processed_filings.models.campaign import CampaignFinanceFilingBase


class Form461FilingBase(CampaignFinanceFilingBase):
    """
    Base and abstract model for Form 461 filings.
    """
    statement_type = models.CharField(
        max_length=50,
        verbose_name='statement type',
        help_text='Type of statement, e.g., "Quarterly", "Semi-Annual", Pre-'
                  'Election (from CVR_CAMPAIGN_DISCLOSURE.STMT_TYPE)',
    )
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

    class Meta:
        """
        Model options.
        """
        app_label = 'calaccess_processed_filings'
        abstract = True

    def __str__(self):
        return str(self.filing_id)


class Form461Filing(Form461FilingBase):
    """
    The most recent version of each Form 461 filing by independent expenditure or major donor committees.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        primary_key=True,
        null=False,
        help_text='Unique identification number for the Form 461 filing ('
                  'from CVR_CAMPAIGN_DISCLOSURE_CD.FILING_ID)',
    )
    amendment_count = models.IntegerField(
        verbose_name='Count amendments',
        db_index=True,
        null=False,
        help_text='Number of amendments to the Form 461 filing (from '
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
        verbose_name = "Form 461 (Campaign Disclosure) filing"

    def __str__(self):
        return str(self.filing_id)


class Form461FilingVersion(Form461FilingBase):
    """
    Every version of each Form 461 filing by independent expenditure or major donor committees.
    """
    filing = models.ForeignKey(
        'Form461Filing',
        related_name='versions',
        db_constraint=False,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Unique identification number for the Form 461 filing ('
                  'from CVR_CAMPAIGN_DISCLOSURE_CD.FILING_ID)',
    )
    amend_id = models.IntegerField(
        verbose_name='amendment id',
        null=False,
        help_text='Identifies the version of the Form 461 filing, with 0 '
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
        verbose_name = "Form 461 (Campaign Disclosure) filing version"

    def __str__(self):
        return '%s-%s' % (self.filing, self.amend_id)
