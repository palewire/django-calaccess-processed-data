#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing Part 3 data from Schedule 496, the Late Independent Expenditure Reports.

More about the filing: https://calaccess.californiacivicdata.org/documentation/calaccess-forms/f496/
"""
from django.db import models
from calaccess_processed_filings.models.campaign import CampaignContributionBase


class Form496Part3ItemBase(CampaignContributionBase):
    """
    Abstract base model for items reported on Schedule A of Form 460 filings.

    On Schedule A, campaign filers are required to itemize monetary
    contributions received during the period covered by the filing.
    """
    amount = models.DecimalField(
        verbose_name='amount',
        decimal_places=2,
        max_digits=14,
        help_text="Amount received from the contributor in the period covered "
                  "by the filing (from RCPT_CD.AMOUNT)"
    )
    interest_rate = models.CharField(
        verbose_name='interest rate',
        max_length=30,
        blank=True,
        help_text='Interest rate of a loan. This is sometimes expressed as a '
                  'decimal (e.g., 0.10) and other times as a percent (e.g., '
                  '10.0% (from RCPT_CD.INT_RATE)'
    )

    class Meta:
        """
        Model options.
        """
        app_label = 'calaccess_processed_filings'
        abstract = True


class Form496Part3Item(Form496Part3ItemBase):
    """
    Monetary contributions of greater than $100 from the Form 496's Part 3.
    """
    filing = models.ForeignKey(
        'Form496Filing',
        related_name='part3_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 496 on which the monetary'
                  ' contribution was reported (from RCPT_CD.FILING_ID)',
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
        verbose_name = "Form 496 (Late Independent Expenditure) Part 3 item"

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


class Form496Part3ItemVersion(Form496Part3ItemBase):
    """
    Every version of monetary contributions of greater than $100 from the Form 496's Part 3.
    """
    filing_version = models.ForeignKey(
        'Form496FilingVersion',
        related_name='part3_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 496 that includes the received contribution'
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
        verbose_name = "Form 496 (Late Independent Expenditure) Part 3 item version"

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )
