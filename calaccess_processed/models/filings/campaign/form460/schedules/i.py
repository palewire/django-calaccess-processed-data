#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Campaign Disclosure Statements (Form 460).
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.filings.campaign import CampaignContributionBase


class Form460ScheduleIItemBase(CampaignContributionBase):
    """
    Abstract base model for items reported on Schedule I of Form 460 filings.

    On Schedule I, campaign filers are required to report miscellaneous cash
    increases during the period covered by the filing. These include any
    transaction that increases the cash position of the filer, but is not a
    monetary contribution, loan, or loan repayment.
    """
    amount = models.DecimalField(
        verbose_name='amount',
        decimal_places=2,
        max_digits=14,
        help_text="Amount of cash increase from the contributor in the period "
                  "covered by the filing (from RCPT_CD.AMOUNT)"
    )
    receipt_description = models.CharField(
        verbose_name='receipt description',
        max_length=90,
        blank=True,
        help_text="Description of the cash increase (from RCPT_CD.CTRIB_DSCR)"
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class Form460ScheduleIItem(Form460ScheduleIItemBase):
    """
    Miscellaneous cash increases to the coffers of campaign filers.

    Includes any transaction that increases the cash position of the filer, but
    is not a monetary contribution, loan, or loan repayment.

    These transactions are itemized on Schedule I of the most recent version
    of each Form 460 filing. For miscellaneous cash increases itemized on any
    version of any Form 460 filing, see Form460ScheduleIItemVersion.

    Derived from RCPT_CD records where FORM_TYPE is 'I'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_i_items',
        null=True,
        on_delete=models.SET_NULL,
        db_constraint=False,
        help_text='Foreign key referring to the Form 460 on which the '
                  'miscellaneous cash increase was report (from RCPT_CD.'
                  'FILING_ID)',
    )

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing',
            'line_item',
        ),)
        verbose_name = "Form 460 (Campaign Disclosure) Schedule I item"

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


@python_2_unicode_compatible
class Form460ScheduleIItemVersion(Form460ScheduleIItemBase):
    """
    Every version of each miscellaneous cash increase for a campaign filer.

    Includes any transaction that increases the cash position of the filer, but
    is not a monetary contribution, loan, or loan repayment.

    For miscellaneous cash increases itemized on Schedule I of the most recent
    version of each Form 460 filing, see Form460ScheduleIItem.

    Derived from RCPT_CD records where FORM_TYPE is 'I'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_i_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
                  'includes the miscellaneous cash increase'
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
        verbose_name = "Form 460 (Campaign Disclosure) Schedule I item version"

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )
