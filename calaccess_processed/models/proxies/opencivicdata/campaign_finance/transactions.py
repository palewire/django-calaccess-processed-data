#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for OCD Filing related models..
"""
from __future__ import unicode_literals
import logging
from calaccess_processed.managers import ProcessedDataManager
from calaccess_processed.models import (
    Form460ScheduleAItem,
    Form460ScheduleAItemVersion,
    Form460ScheduleCItem,
    Form460ScheduleCItemVersion
)
from calaccess_processed.sql import execute_custom_sql
from opencivicdata.campaign_finance.models import (
    Transaction,
    TransactionIdentifier
)
from postgres_copy import CopyManager
from psycopg2 import sql
from ..base import OCDProxyModelMixin
logger = logging.getLogger(__name__)


class OCDTransactionManager(ProcessedDataManager):
    """
    Manager with custom methods for OCD Transaction model.
    """
    def load_form460_data(self):
        """
        Load OCD Transactions with data from all Form460 related models.
        """
        logger.info(' Inserting new Transactions...')
        logger.info(' Dropping constraints/indexes')
        self.drop_constraints_and_indexes()

        logger.info(' ...from Form 460 Schedule A Items...')
        logger.info(' ...for current filings...')
        self.insert_contribution_items(
            Form460ScheduleAItem, 'amount', False
        )
        logger.info(' ...for old filings...')
        self.insert_contribution_items(
            Form460ScheduleAItemVersion, 'amount', False
        )

        logger.info(' ...from Form 460 Schedule C Items...')
        logger.info(' ...for current filings...')
        self.insert_contribution_items(
            Form460ScheduleCItem, 'fair_market_value', True
        )
        logger.info(' ...for old filings...')
        self.insert_contribution_items(
            Form460ScheduleCItemVersion, 'fair_market_value', True
        )

        logger.info(' Restoring constraints/indexes')
        self.add_constraints_and_indexes()

    def insert_contribution_items(self, model, amount_field_name, is_in_kind):
        """
        Insert from Form 460 Schedule A Items.

        Insert only current items by default. If current arg is False, insert
        only old items.
        """
        if 'Version' in model._meta.object_name:
            query_name = 'insert_old_transactions_from_form460_contributions'
        else:
            query_name = 'insert_new_transactions_from_form460_contributions'

        source_table = sql.Identifier(
            model._meta.db_table
        )
        source_amount_column = sql.Identifier(
            model._meta.get_field(amount_field_name).column
        )

        execute_custom_sql(
            query_name,
            params={'is_in_kind': is_in_kind},
            composables={
                'source_table': source_table,
                'source_amount_column': source_amount_column,
            },
        )


class OCDTransactionProxy(Transaction, OCDProxyModelMixin):
    """
    A proxy on the OCD Transaction model.
    """
    objects = OCDTransactionManager()

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
