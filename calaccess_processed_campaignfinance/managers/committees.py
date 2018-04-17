#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for OCD Committee related managers.
"""
from __future__ import unicode_literals
import logging
from .base import CampaignFinanceManager
logger = logging.getLogger(__name__)


class OCDCommitteeManager(CampaignFinanceManager):
    """
    Manager with custom methods for OCD Committee model.
    """
    def load(self):
        """
        Load OCD Committee with data extracted from Form460Filing.
        """
        # Updating name of existing committees..
        self.execute_custom_sql('opencivicdata/campaign_finance/committees/update_committee_names_from_form460s')
        # ... and inserting new committees.
        self.execute_custom_sql('opencivicdata/campaign_finance/committees/insert_committees_from_form460s')


class OCDCommitteeIdentifierManager(CampaignFinanceManager):
    """
    Manager with custom methods for OCD CommitteeIdentifier model.
    """
    def load(self):
        """
        Load OCD CommitteeIdentifier with data extracted from Form460Filing.
        """
        #  Insert new committee identifiers.
        self.execute_custom_sql('opencivicdata/campaign_finance/committees/insert_committee_ids_from_form460s')
        # Removing "calaccess_filer_id" from extras field on Committee.
        self.execute_custom_sql('opencivicdata/campaign_finance/committees/remove_calaccess_filer_ids_from_committees')


class OCDCommitteeNameManager(CampaignFinanceManager):
    """
    Manager with custom methods for OCD CommitteeName model.
    """
    def load(self):
        """
        Load OCD CommitteeName with data extracted from Form460Filing.
        """
        # Insert new committee names
        self.execute_custom_sql('opencivicdata/campaign_finance/committees/insert_committee_names_from_form460s')
        # Delete current names from extra list of committee names.
        self.execute_custom_sql('opencivicdata/campaign_finance/committees/delete_current_names_from_committee_names')


class OCDCommitteeTypeManager(CampaignFinanceManager):
    """
    Manager with custom methods for OCD CommitteeType model.
    """
    def load(self):
        """
        Seeds the default data for this model.
        """
        from calaccess_processed_elections.proxies import OCDJurisdictionProxy

        # Prep data
        qs = self.get_queryset()
        jurisdiction = OCDJurisdictionProxy.objects.california()

        # Fire away
        qs.get_or_create(name='Recipient', jurisdiction=jurisdiction)
        qs.get_or_create(name='Candidate', jurisdiction=jurisdiction)
        qs.get_or_create(name='Ballot Measure', jurisdiction=jurisdiction)
