#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Campaign Disclosure Statements (Form 460).
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.base import CalAccessBaseModel
from calaccess_processed.models.filings.campaign import CampaignContributionBase


#
# Summaries
#

class Form460ScheduleASummaryBase(CalAccessBaseModel):
    """
    Abstract base model with summary data from Schedule A attachments to Form 460 filings.

    Includes totals for itemized versus unitemized contributions.
    """
    itemized_contributions = models.FloatField(
        verbose_name='itemized contributions',
        null=True,
        help_text="Amount received this period - contributions of $100 or more. (Include all Schedule A subtotals.)",
    )
    unitemized_contributions = models.FloatField(
        verbose_name='unitemized contributions',
        null=True,
        help_text="Amount received this period - unitemized contributions of less than $100",
    )
    total_contributions = models.FloatField(
        verbose_name='total contributions',
        null=True,
        help_text="Total monetary contributions received this period. (Add Lines 1 and 2. Enter here and on summary \
Page, Column A, Line 1.)",
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


class Form460ScheduleASummary(Form460ScheduleASummaryBase):
    """
    The summary data included with the most recent version a Schedule A attachment to a Form 460 filing.

    Includes totals for itemized versus unitemized contributions.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_a_summaries',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the summary was reported',
    )

    class Meta:
        """
        Model options.
        """
        verbose_name = "Form 460 (Campaign Disclosure) Schedule A summary"
        verbose_name_plural = "Form 460 (Campaign Disclosure) Schedule A summaries"

    def __str__(self):
        return '%s' % (self.filing)


class Form460ScheduleASummaryVersion(Form460ScheduleASummaryBase):
    """
    The summary data included with each version of a Schedule A attachment to a Form 460 filing.

    Includes totals for itemized versus unitemized contributions.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_a_summaries',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the summary'
    )

    class Meta:
        """
        Model options.
        """
        verbose_name = "Form 460 (Campaign Disclosure) Schedule A summary version"

    def __str__(self):
        return '%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
        )


#
# Items
#

class Form460ScheduleAItemBase(CampaignContributionBase):
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

    class Meta:
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleAItem(Form460ScheduleAItemBase):
    """
    Monetary contributions received by campaign filers.

    These transactions are itemized on Schedule A of the most recent version
    of each Form 460 filing. For monetary contributions itemized on any version
    of any Form 460 filing, see Form460ScheduleAItemVersion.

    Also includes contributions transferred to special election commitees,
    which were itemized on Schedule A-1 until around 2001.

    Derived from RCPT_CD records where FORM_TYPE is 'A' or 'A-1'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_a_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the monetary'
                  ' contribution was reported (from RCPT_CD.FILING_ID)',
    )

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing',
            'line_item',
        ),)
        verbose_name = "Form 460 (Campaign Disclosure) Schedule A item"

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleAItemVersion(Form460ScheduleAItemBase):
    """
    Every version of each monetary contribution received by a campaign filer.

    For monetary contributions itemized on Schedule A of the most recent
    version of each Form 460 filing, see Form460ScheduleAItem.

    Derived from RCPT_CD records where FORM_TYPE is 'A' or 'A-1'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_a_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the received contribution'
    )

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
        verbose_name = "Form 460 (Campaign Disclosure) Schedule A item version"

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )
