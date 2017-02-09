#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Campaign Disclosure Statements (Form 460).
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.managers import ProcessedDataManager
from calaccess_processed.models.filings.campaign import CampaignContributionBase


class Form460ScheduleCItemBase(CampaignContributionBase):
    """
    Abstract base model for items reported on Schedule C of Form 460 filings.

    On Schedule C, campaign filers are required to itemize nonmonetary
    contributions received during the period covered by the filing.
    """
    fair_market_value = models.DecimalField(
        verbose_name='fair market value',
        decimal_places=2,
        max_digits=14,
        help_text="Amount it would cost to purchase the donated goods or "
                  "services on the open market (from RCPT_CD.AMOUNT)"
    )
    contribution_description = models.CharField(
        max_length=90,
        blank=True,
        help_text="Description of the contributed goods or services (from "
                  "RCPT_CD.CTRIB_DSCR)"
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleCItem(Form460ScheduleCItemBase):
    """
    Nonmonetary contributions received by campaign filers.

    These transactions are itemized on Schedule C of the most recent version
    of each Form 460 filing. For nonmonetary contributions itemized on any
    version of any Form 460 filing, see Form460ScheduleCItemVersion.

    Derived from RCPT_CD records where FORM_TYPE is 'C'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_c_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the monetary'
                  ' contribution was reported (from RCPT_CD.FILING_ID)',
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
class Form460ScheduleCItemVersion(Form460ScheduleCItemBase):
    """
    Every version of each nonmonetary contribution received by a campaign filer.

    For nonmonetary contributions itemized on Schedule C of the most recent
    version of each Form 460 filing, see Form460ScheduleCItem.

    Derived from RCPT_CD records where FORM_TYPE is 'C'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_c_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the received contribution'
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
