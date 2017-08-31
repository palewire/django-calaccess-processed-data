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

class Form460ScheduleCSummaryBase(CalAccessBaseModel):
    """
    Abstract base model with summary data from Schedule C attachments to Form 460 filings.

    Includes totals for itemized versus unitemized non-monetary contributions.
    """
    itemized_contributions = models.FloatField(
        verbose_name='itemized contributions',
        null=True,
        help_text="Amount received this period - itemized nonmonetary contributions. \
(Include all Schedule C subtotals)",
    )
    unitemized_contributions = models.FloatField(
        verbose_name='unitemized contributions',
        null=True,
        help_text="Amount received this period - unitemized nonmonetary contributions of less than $100",
    )
    total_contributions = models.FloatField(
        verbose_name='total contributions',
        null=True,
        help_text="Total nonmonetary contributions received this period. (Add Lines 1 and 2. Enter here and on the \
Summary Page, Column A, Lines 4 and 10.)",
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


class Form460ScheduleCSummary(Form460ScheduleCSummaryBase):
    """
    The summary data included with the most recent version a Schedule C attachment to a Form 460 filing.

    Includes totals for itemized versus unitemized non-monetary contributions.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_c_summaries',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the summary was reported',
    )

    class Meta:
        """
        Model options.
        """
        verbose_name = "Form 460 (Campaign Disclosure) Schedule C summary"
        verbose_name_plural = "Form 460 (Campaign Disclosure) Schedule C summaries"

    def __str__(self):
        return '%s' % (self.filing)


class Form460ScheduleCSummaryVersion(Form460ScheduleCSummaryBase):
    """
    The summary data included with each version of a Schedule C attachment to a Form 460 filing.

    Includes totals for itemized versus unitemized non-monetary contributions.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_c_summaries',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the summary'
    )

    class Meta:
        """
        Model options.
        """
        verbose_name = "Form 460 (Campaign Disclosure) Schedule C summary version"

    def __str__(self):
        return '%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
        )


#
# Items
#

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

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing',
            'line_item',
        ),)
        verbose_name = "Form 460 (Campaign Disclosure) Schedule C item"

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
        verbose_name = "Form 460 (Campaign Disclosure) Schedule C item version"

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )
