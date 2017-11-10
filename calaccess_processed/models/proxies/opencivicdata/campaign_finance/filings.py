#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for OCD Filing related models..
"""
from __future__ import unicode_literals
import logging
from calaccess_processed.sql import execute_custom_sql
from opencivicdata.campaign_finance.models import (
    Filing,
    FilingAction,
    FilingActionSummaryAmount,
    FilingIdentifier,
    FilingSource,
    Transaction,
    TransactionIdentifier,
)
from postgres_copy import CopyManager
from ..base import OCDProxyModelMixin
logger = logging.getLogger(__name__)


class OCDFilingManager(CopyManager):
    """
    Manager with custom methods for OCD Filing model.
    """
    def load_form460_data(self):
        """
        Load OCD Filing with data extracted from Form460Filing.
        """
        logger.info(' Updating existing Filings...')
        logger.info(' ...coverage_start_date...')

        execute_custom_sql(
            'update_filings_from_form460s',
            to_update='coverage_start_date',
            source_table='calaccess_processed_form460filing',
            source_column='from_date',
        )
        logger.info(' ...coverage_end_date...')
        execute_custom_sql(
            'update_filings_from_form460s',
            to_update='coverage_end_date',
            source_table='calaccess_processed_form460filing',
            source_column='thru_date',
        )
        logger.info(' ...filer_id...')
        execute_custom_sql(
            'update_filings_from_form460s',
            to_update='filer_id',
            source_table='opencivicdata_committeeidentifier',
            source_column='committee_id',
        )

        logger.info(' Inserting new Filings...')
        execute_custom_sql('insert_filings_from_form460s')


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


class OCDFilingIdentifierManager(CopyManager):
    """
    Manager with custom methods for OCD FilingIdentifier model.
    """
    def load_form460_data(self):
        """
        Load OCD FilingIdentifier with data extracted from Form460Filing.
        """
        logger.info(' Inserting new Filing Identifiers...')
        execute_custom_sql('insert_filing_ids_from_form460s')
        logger.info(
            ' Removing "calaccess_filing_id" from extras field on Filing...'
        )
        execute_custom_sql('remove_calaccess_filing_ids_from_filings')


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


class OCDFilingActionManager(CopyManager):
    """
    Manager with custom methods for OCD FilingAction model.
    """
    def load_form460_data(self):
        """
        Load OCD FilingAction with data extracted from Form460FilingVersion.
        """
        logger.info(' Inserting new Filing Actions...')
        execute_custom_sql('insert_filing_actions_from_form460s')


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
    objects = CopyManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDTransactionProxy(Transaction, OCDProxyModelMixin):
    """
    A proxy on the OCD Transaction model.
    """
    objects = CopyManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDTransactionIdentifierProxy(TransactionIdentifier, OCDProxyModelMixin):
    """
    A proxy on the OCD TransactionIdentifier model.
    """
    objects = CopyManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
