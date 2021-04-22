#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Campaign Disclosure Statements (Form 461) Part 5 schedules.
"""
from django.db import models
from calaccess_processed_filings.models.campaign import CampaignExpenditureItemBase


class Form461Part5Item(CampaignExpenditureItemBase):
    """
    Payments made by Form 461 filers.
    """
    filing = models.ForeignKey(
        'Form461Filing',
        related_name='part_5_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 461 on which the '
                  'payment was reported (from EXPN_CD.FILING_ID)',
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
        verbose_name = "Form 461 (Campaign Disclosure) Part 5 item"

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


class Form461Part5ItemVersion(CampaignExpenditureItemBase):
    """
    Every version of each payment made by a Form 461 filing.
    """
    filing_version = models.ForeignKey(
        'Form461FilingVersion',
        related_name='part_5_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 461 that '
                  'includes the payment made'
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
        verbose_name = "Form 461 (Campaign Disclosure) Part 5 item version"

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )
