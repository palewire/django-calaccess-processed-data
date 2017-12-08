#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for OCD Filing related models..
"""
from __future__ import unicode_literals
import logging
from calaccess_processed.sql import execute_custom_sql
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
logger = logging.getLogger(__name__)


class OCDCommitteeManager(CopyManager):
    """
    Manager with custom methods for OCD Committee model.
    """
    def load_form460_data(self):
        """
        Load OCD Committee with data extracted from Form460Filing.
        """
        logger.info(' Updating name of existing Committees...')
        execute_custom_sql('update_committee_names_from_form460s')
        logger.info(' Inserting new Committees...')
        execute_custom_sql('insert_committees_from_form460s')


class OCDCommitteeProxy(Committee, OCDProxyModelMixin):
    """
    Proxy of the OCD Committee model.
    """
    objects = OCDCommitteeManager()

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
        logger.info(' Inserting new Committee Identifiers...')
        execute_custom_sql('insert_committee_ids_from_form460s')
        logger.info(
            ' Removing "calaccess_filer_id" from extras field on Committee...'
        )
        execute_custom_sql('remove_calaccess_filer_ids_from_committees')


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
        logger.info(' Inserting new Committee Names...')
        execute_custom_sql('insert_committee_names_from_form460s')
        logger.info(' Deleting current names from Committee Names...')
        execute_custom_sql('delete_current_names_from_committee_names')


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
        Returns the recipient CommitteeType.
        """
        logger.info(' Creating Committee Types...')

        self.get_queryset().get_or_create(
            name='Recipient',
            jurisdiction=OCDJurisdictionProxy.objects.california(),
        )[0]
        self.get_queryset().get_or_create(
            name='Candidate',
            jurisdiction=OCDJurisdictionProxy.objects.california(),
        )[0]
        self.get_queryset().get_or_create(
            name='Ballot Measure',
            jurisdiction=OCDJurisdictionProxy.objects.california(),
        )[0]


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
