#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for OCD Filing related models..
"""
from __future__ import unicode_literals
import logging
from opencivicdata.campaign_finance.models import (
    Committee,
    CommitteeType,
    CommitteeIdentifier,
    CommitteeName,
    CommitteeSource,
)
from calaccess_processed.managers import (
    OCDCommitteeManager,
    OCDCommitteeIdentifierManager,
    OCDCommitteeNameManager,
    OCDCommitteeTypeManager
)
from postgres_copy import CopyManager
from ..base import OCDProxyModelMixin
logger = logging.getLogger(__name__)


class OCDCommitteeProxy(Committee, OCDProxyModelMixin):
    """
    Proxy of the OCD Committee model.
    """
    objects = OCDCommitteeManager()

    @property
    def calaccess_filer_id(self):
        """
        Returns the committee's CAL-ACCESS filer id.
        """
        return self.identifiers.get(scheme="calaccess_filer_id")

    @property
    def calaccess_filer_url(self):
        """
        Returns the URL of the committee's detail page on the CAL-ACCESS website.
        """
        url_template = "http://cal-access.sos.ca.gov/Campaign/Committees/Detail.aspx?id={}"
        return url_template.format(self.calaccess_filer_id.identifier)

    @property
    def filing_proxies(self):
        """
        A QuerySet of OCDCandidateContestProxy for the election.
        """
        from .filings import OCDFilingProxy
        return OCDFilingProxy.objects.filter(filer=self)

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDCommitteeIdentifierProxy(CommitteeIdentifier, OCDProxyModelMixin):
    """
    Proxy of the OCD CommitteeIdentifier model.
    """
    objects = OCDCommitteeIdentifierManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDCommitteeNameProxy(CommitteeName, OCDProxyModelMixin):
    """
    Proxy of the OCD CommitteeName model.
    """
    objects = OCDCommitteeNameManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDCommitteeSourceProxy(CommitteeSource, OCDProxyModelMixin):
    """
    Proxy of the OCD CommitteeSource model.
    """
    objects = CopyManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDCommitteeTypeProxy(CommitteeType, OCDProxyModelMixin):
    """
    Proxy of the OCD CommitteeSource model.
    """
    objects = OCDCommitteeTypeManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
