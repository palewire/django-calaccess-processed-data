#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for OCD Transaction related managers.
"""
from __future__ import unicode_literals
import logging
from psycopg2 import sql
from .base import CampaignFinanceManager
logger = logging.getLogger(__name__)


class OCDTransactionManager(CampaignFinanceManager):
    """
    Manager with custom methods for OCD Transaction model.
    """
    def execute(self):
        """
        Load OCD Transactions with data from all Form460 related models.
        """
        from calaccess_processed_filings.models import (
            Form460ScheduleAItem,
            Form460ScheduleAItemVersion,
            Form460ScheduleCItem,
            Form460ScheduleCItemVersion
        )

        # ...from Form 460 Schedule A Items...
        # ...for current filings...
        self.insert_contribution_items(
            Form460ScheduleAItem, 'amount', False
        )
        # ...for old filings...
        self.insert_contribution_items(
            Form460ScheduleAItemVersion, 'amount', False
        )

        # ...from Form 460 Schedule C Items...
        # ...for current filings...
        self.insert_contribution_items(
            Form460ScheduleCItem, 'fair_market_value', True
        )
        # ...for old filings...
        self.insert_contribution_items(
            Form460ScheduleCItemVersion, 'fair_market_value', True
        )

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

        source_table = sql.Identifier(model._meta.db_table)
        source_amount_field = model._meta.get_field(amount_field_name)
        source_amount_column = sql.Identifier(source_amount_field.column)

        self.execute_custom_sql(
            "opencivicdata/campaign_finance/transactions/" + query_name,
            params={'is_in_kind': is_in_kind},
            composables={
                'source_table': source_table,
                'source_amount_column': source_amount_column,
            },
        )
