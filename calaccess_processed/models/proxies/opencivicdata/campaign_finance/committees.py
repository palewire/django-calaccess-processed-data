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
from postgres_copy import CopyManager
from ..base import OCDProxyModelMixin
from ..core.jurisdictions import OCDJurisdictionProxy
from calaccess_processed.sql import execute_custom_sql
logger = logging.getLogger(__name__)


class OCDCommitteeManager(CopyManager):
    """
    Manager with custom methods for OCD Committee model.
    """
    def load_form460_data(self):
        """
        Load OCD Committee with data extracted from Form460Filing.
        """
        # Updating name of existing committees..
        execute_custom_sql('opencivicdata/campaign_finance/committees/update_committee_names_from_form460s')
        # ... and inserting new committees.
        execute_custom_sql('opencivicdata/campaign_finance/committees/insert_committees_from_form460s')


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


class OCDCommitteeIdentifierManager(CopyManager):
    """
    Manager with custom methods for OCD CommitteeIdentifier model.
    """
    def load_form460_data(self):
        """
        Load OCD CommitteeIdentifier with data extracted from Form460Filing.
        """
        #  Insert new committee identifiers.
        execute_custom_sql('opencivicdata/campaign_finance/committees/insert_committee_ids_from_form460s')
        # Removing "calaccess_filer_id" from extras field on Committee.
        execute_custom_sql('opencivicdata/campaign_finance/committees/remove_calaccess_filer_ids_from_committees')


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


class OCDCommitteeNameManager(CopyManager):
    """
    Manager with custom methods for OCD CommitteeName model.
    """
    def load_form460_data(self):
        """
        Load OCD CommitteeName with data extracted from Form460Filing.
        """
        # Insert new committee names
        execute_custom_sql('opencivicdata/campaign_finance/committees/insert_committee_names_from_form460s')
        # Delete current names from extra list of committee names.
        execute_custom_sql('opencivicdata/campaign_finance/committees/delete_current_names_from_committee_names')


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


class OCDCommitteeTypeManager(CopyManager):
    """
    Manager with custom methods for OCD CommitteeType model.
    """
    def seed(self):
        """
        Seeds the default data for this model.
        """
        # Prep data
        qs = self.get_queryset()
        jurisdiction = OCDJurisdictionProxy.objects.california()

        # Fire away
        qs.get_or_create(name='Recipient', jurisdiction=jurisdiction)
        qs.get_or_create(name='Candidate', jurisdiction=jurisdiction)
        qs.get_or_create(name='Ballot Measure', jurisdiction=jurisdiction)


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
