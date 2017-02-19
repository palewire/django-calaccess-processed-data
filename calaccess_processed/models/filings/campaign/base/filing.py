#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Abstract base models for campaign finance-related filings and transactions.
"""
from __future__ import unicode_literals
from django.db import models
from calaccess_processed.models.base import CalAccessBaseModel


class CampaignFinanceFilingBase(CalAccessBaseModel):
    """
    Base and abstract model for campaign finance-related filings.
    """
    date_filed = models.DateField(
        verbose_name='date filed',
        db_index=True,
        null=False,
        help_text="Date this report was filed, according to the filer "
                  "(from CVR_CAMPAIGN_DISCLOSURE.RPT_DATE)",
    )
    filer_id = models.IntegerField(
        verbose_name='filer id',
        db_index=True,
        null=False,
        help_text="Numeric filer identification number (from FILER_XREF.FILER_ID)",
    )
    filer_lastname = models.CharField(
        verbose_name='filer last name',
        max_length=200,
        null=False,
        blank=False,
        help_text="Last name of filer (from CVR_CAMPAIGN_DISCLOSURE.FILER_NAML)",
    )
    filer_firstname = models.CharField(
        verbose_name="filer first name",
        max_length=45,
        null=False,
        blank=True,
        help_text="First name of the filer (from "
                  "CVR_CAMPAIGN_DISCLOSURE.FILER_NAMF)",
    )
    election_date = models.DateField(
        verbose_name='election date',
        db_index=True,
        null=True,
        help_text="Date of the election in which the filer is participating "
                  "(from CVR_CAMPAIGN_DISCLOSURE.ELECT_DATE)",
    )

    class Meta:
        """
        Model options.
        """
        app_label = 'calaccess_processed'
        abstract = True
