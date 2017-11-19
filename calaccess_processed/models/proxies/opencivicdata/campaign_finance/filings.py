#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for OCD Filing related models..
"""
from __future__ import unicode_literals
import logging
from calaccess_processed.managers import ProcessedDataManager
from calaccess_processed.models import (
    Form460Filing,
    Form460FilingVersion,
    Form460ScheduleAItem,
    Form460ScheduleAItemVersion,
    Form460ScheduleASummaryVersion,
    Form460ScheduleCItem,
    Form460ScheduleCItemVersion,
    Form460ScheduleCSummaryVersion,
)
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
from psycopg2 import sql
from ..base import OCDProxyModelMixin
logger = logging.getLogger(__name__)


class OCDFilingManager(CopyManager):
    """
    Manager with custom methods for OCD Filing model.
    """
    def _update_filings_from_form460_field(self, target_column, source_column):
        """
        Update target_column on OCD Filing with value from source_column.
        """
        target_field = Filing._meta.get_field(target_column)
        logger.info(' ...%s...' % target_field.verbose_name)
        source_table_identifier = sql.Identifier(
            Form460Filing._meta.db_table
        )
        source_column_identifier = sql.Identifier(
            Form460Filing._meta.get_field(source_column).column
        )
        target_column_identifier = sql.Identifier(
            Filing._meta.get_field(target_column).column
        )
        execute_custom_sql(
            'update_filings_from_formfiling_table',
            composables={
                'source_table': source_table_identifier,
                'source_column': source_column_identifier,
                'target_column': target_column_identifier,
            },
        )

    def _update_filings_filer_id(self, model):
        """
        Update filer_id on OCD Filings.
        """
        processed_data_table_identifier = sql.Identifier(
            model._meta.db_table
        )
        logger.info(' ...filer id...')
        execute_custom_sql(
            'update_filings_filer_id',
            composables={
                'processed_data_table': processed_data_table_identifier,
            },
        )

    def load_form460_data(self):
        """
        Load OCD Filing with data extracted from Form460Filing.
        """
        logger.info(' Updating existing Filings...')
        self._update_filings_from_form460_field(
            'coverage_start_date', 'from_date',
        )
        self._update_filings_from_form460_field(
            'coverage_end_date', 'thru_date',
        )
        self._update_filings_filer_id(Form460Filing)

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

        logger.info(' Setting is_current false on actions of amended Filings...')
        execute_custom_sql('set_is_current_for_old_filing_actions')

        logger.info(' Setting is_current true on latest Filing Actions...')
        execute_custom_sql('set_is_current_for_new_filing_actions')


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


class OCDFilingActionSummaryAmountManager(CopyManager):
    """
    Manager with custom methods for OCD FilingActionSummaryAmount model.
    """
    def _load_form460_summary_sheet_data(self):
        """
        Load OCD FilingActionSummaryAmount with data extracted from Form460FilingVersion.
        """
        sum_fields = [
            f for f in Form460FilingVersion._meta.get_fields()
            if f.__class__.__name__ == 'IntegerField' and
            f.name[-3:] != '_id'
        ]
        table_composable = sql.Identifier(Form460FilingVersion._meta.db_table)
        for f in sum_fields:
            label_words = [w.capitalize() for w in f.name.split('_')]
            label = ' '.join(label_words)
            logger.info(' ...%s...' % label)
            execute_custom_sql(
                'insert_filing_action_summary_amounts',
                params={'label': label},
                composables={
                    'source_table': table_composable,
                    'source_column': sql.Identifier(f.column),
                }
            )

    def _load_from_form460_schedule_summary_field(self, model, label, field_name):
        """
        Load OCD FilingActionSummaryAmount with from a schedule summary field.
        """
        source_table_identifier = sql.Identifier(model._meta.db_table)
        source_column_identifier = sql.Identifier(
            model._meta.get_field(field_name).column
        )

        logger.info(' ...%s...' % label)

        execute_custom_sql(
            'insert_filing_action_summary_amount_from_schedules',
            params={'label': label},
            composables={
                'source_table': source_table_identifier,
                'source_column': source_column_identifier,
            },
        )

    def load_form460_data(self):
        """
        Load OCD FilingActionSummaryAmount with data from all Form460 related models.
        """
        logger.info(' Inserting new Filing Action Summary Amounts...')
        logger.info(' ...from Form 460 Summary Sheet...')
        self._load_form460_summary_sheet_data()

        logger.info(' ...from Form 460 Schedule A Summary...')
        self._load_from_form460_schedule_summary_field(
            Form460ScheduleASummaryVersion,
            'Itemized Monetary Contributions',
            'itemized_contributions',
        )
        self._load_from_form460_schedule_summary_field(
            Form460ScheduleASummaryVersion,
            'Unitemized Monetary Contributions',
            'unitemized_contributions',
        )

        logger.info(' ...from Form 460 Schedule C Summary...')
        self._load_from_form460_schedule_summary_field(
            Form460ScheduleCSummaryVersion,
            'Itemized Non-monetary Contributions',
            'itemized_contributions',
        )
        self._load_from_form460_schedule_summary_field(
            Form460ScheduleCSummaryVersion,
            'Unitemized Non-monetary Contributions',
            'unitemized_contributions',
        )


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
