#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing data from Campaign Disclosure Statements (Form 460).
"""
from django.db import models
from calaccess_processed_filings.models.campaign import CampaignExpenditureItemBase


class Form460ScheduleDItemBase(CampaignExpenditureItemBase):
    """
    Abstract base model for items reported on Schedule D of Form 460 filings.

    On Schedule D, campaign filers are required to summarize contributions
    and independent expenditures in support or opposition to other candidates
    and ballot measures.
    """
    cumulative_election_amount = models.DecimalField(
        decimal_places=2,
        max_digits=14,
        null=True,
        help_text="If the candidate is subject to contribution limits, the "
                  "cumulative amount given by the filer during the election "
                  "cycle as of the Form 460's filing date (from EXPN_CD."
                  "CUM_OTH)"
    )

    class Meta:
        """
        Model options.
        """
        app_label = 'calaccess_processed_filings'
        abstract = True


class Form460ScheduleDItem(Form460ScheduleDItemBase):
    """
    Payments in support or opposition of other candidates and ballot measures.

    These transactions are itemized on Schedule D of the most recent version
    of each Form 460 filing. For payments itemized on any version of any Form
    460 filing, see Form460ScheduleDItemVersion.

    Derived from EXPN_CD records where FORM_TYPE is 'D'.
    """
    filing = models.ForeignKey(
        'Form460Filing',
        related_name='schedule_d_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the Form 460 on which the '
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
        verbose_name = "Form 460 (Campaign Disclosure) Schedule D item"

    def __str__(self):
        return '%s-%s' % (self.filing, self.line_item)


class Form460ScheduleDItemVersion(Form460ScheduleDItemBase):
    """
    Every version of each payment supporting/opposing another candidate/ballot measure.

    For payments itemized on Schedule D of the most recent version of each Form
    460 filing, see Form460ScheduleDItem.

    Derived from EXPN_CD records where FORM_TYPE is 'D'.
    """
    filing_version = models.ForeignKey(
        'Form460FilingVersion',
        related_name='schedule_d_items',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the version of the Form 460 that '
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
        verbose_name = "Form 460 (Campaign Disclosure) Schedule D item version"

    def __str__(self):
        return '%s-%s-%s' % (
            self.filing_version.filing_id,
            self.filing_version.amend_id,
            self.line_item
        )
