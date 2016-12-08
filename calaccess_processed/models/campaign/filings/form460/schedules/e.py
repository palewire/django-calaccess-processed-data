#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Campaign Disclosure Statements (Form 460).
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.managers import ProcessedDataManager
from calaccess_processed.models.campaign.filings import (
    CampaignExpenditureItemBase,
    CampaignExpenditureSubItemBase,
)


@python_2_unicode_compatible
class Form460ScheduleEItem(CampaignExpenditureItemBase):
    """
    Payments made by campaign filers.

    These transactions are itemized on Schedule E of the most recent version
    of each Form 460 filing. For payments itemized on any version of any
    filing, see Form460ScheduleEItemVersion.

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
        'Form460Filing',
        related_name='schedule_e_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the '
                  'payment was reported (from EXPN_CD.FILING_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleEItemVersion(CampaignExpenditureItemBase):
    """
    Every version of each payment made by a campaign filer.

    For payments itemized on Schedule E of the most recent version of each Form
    460 filing, see Form460ScheduleEItem.

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
        'Form460FilingVersion',
        related_name='schedule_e_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the payment made'
    )

    objects = ProcessedDataManager()

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

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )


@python_2_unicode_compatible
class Form460ScheduleESubItem(CampaignExpenditureSubItemBase):
    """
    Sub-items of payments made by campaign filers.

    These transactions are itemized on Schedule E of the most recent version
    of each Form 460 filing. For sub-item payments on any version of any Form
    460 filing, see Form460ScheduleESubItemVersion.

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
        'Form460Filing',
        related_name='schedule_e_subitems',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the '
                  'payment was reported (from EXPN_CD.FILING_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing',
            'line_item',
        ),)

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleESubItemVersion(CampaignExpenditureSubItemBase):
    """
    Every version of each sub-item of a payment by a campaign filer.

    For payments sub-itemized on Schedule E of the most recent version of each
    Form 460 filing, see Form460ScheduleESubItem.

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
        'Form460FilingVersion',
        related_name='schedule_e_subitems',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the payment made'
    )

    objects = ProcessedDataManager()

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

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )
