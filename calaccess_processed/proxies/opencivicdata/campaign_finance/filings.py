#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for OCD Filing related models..
"""
from __future__ import unicode_literals
import logging
from calaccess_processed.managers import (
    OCDFilingManager,
    OCDFilingIdentifierManager,
    OCDFilingActionManager,
    OCDFilingActionSummaryAmountManager
)
from opencivicdata.campaign_finance.models import (
    Filing,
    FilingAction,
    FilingActionSummaryAmount,
    FilingIdentifier,
    FilingSource
)
from postgres_copy import CopyManager
from ..base import OCDProxyModelMixin
logger = logging.getLogger(__name__)


class OCDFilingProxy(Filing, OCDProxyModelMixin):
    """
    A proxy on the OCD Filing model.
    """
    objects = OCDFilingManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True

    @property
    def current_action(self):
        """
        Returns the most current action linked with this filing.
        """
        return self.actions.get(is_current=True)

    @property
    def calaccess_filing_id(self):
        """
        Returns the filing's CAL-ACCESS filing ID.
        """
        return self.identifiers.get(scheme="calaccess_filing_id")

    @property
    def calaccess_amend_id(self):
        """
        Returns the filing's CAL-ACCESS amendment id.
        """
        return self.current_action.extras['amend_id']

    @property
    def calaccess_filing_url(self):
        """
        Returns the filing's URL on the CAL-ACCESS website.
        """
        url_template = "http://cal-access.sos.ca.gov/PDFGen/pdfgen.prg?filingid={}&amendid={}"
        return url_template.format(
            self.calaccess_filing_id.identifier,
            self.calaccess_amend_id
        )

    @property
    def calaccess_filer_id(self):
        """
        Returns the filer's CAL-ACCESS filer id.
        """
        return self.filer.identifiers.get(scheme="calaccess_filer_id")

    @property
    def calaccess_filer_url(self):
        """
        Returns the URL of the filer's detail page on the CAL-ACCESS website.
        """
        url_template = "http://cal-access.sos.ca.gov/Campaign/Committees/Detail.aspx?id={}"
        return url_template.format(self.calaccess_filer_id.identifier)


class OCDFilingIdentifierProxy(FilingIdentifier, OCDProxyModelMixin):
    """
    A proxy on the OCD FilingIdentifier model.
    """
    objects = OCDFilingIdentifierManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDFilingSourceProxy(FilingSource, OCDProxyModelMixin):
    """
    A proxy on the OCD FilingSource model.
    """
    objects = CopyManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDFilingActionProxy(FilingAction, OCDProxyModelMixin):
    """
    A proxy on the OCD FilingAction model.
    """
    objects = OCDFilingActionManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDFilingActionSummaryAmountProxy(FilingActionSummaryAmount, OCDProxyModelMixin):
    """
    A proxy on the OCD FilingActionSummaryAmount model.
    """
    objects = OCDFilingActionSummaryAmountManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
