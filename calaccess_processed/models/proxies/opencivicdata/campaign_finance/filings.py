#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for OCD Filing related models..
"""
from __future__ import unicode_literals
import logging
from calaccess_processed.models import (
    Form460FilingVersion,
    Form460ScheduleASummaryVersion,
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
            identifiers={
                'to_update': 'coverage_start_date',
                'source_table': 'calaccess_processed_form460filing',
                'source_column': 'from_date',
            }
        )
        logger.info(' ...coverage_end_date...')
        execute_custom_sql(
            'update_filings_from_form460s',
            identifiers={
                'to_update': 'coverage_start_date',
                'source_table': 'calaccess_processed_form460filing',
                'source_column': 'from_date',
            }
        )
        logger.info(' ...filer_id...')
        execute_custom_sql(
            'update_filings_from_form460s',
            identifiers={
                'to_update': 'coverage_start_date',
                'source_table': 'calaccess_processed_form460filing',
                'source_column': 'from_date',
            }
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
        for f in sum_fields:
            label_words = [w.capitalize() for w in f.name.split('_')]
            label = ' '.join(label_words)
            logger.info(' ...%s...' % label)
            execute_custom_sql(
                'insert_filing_action_summary_amounts',
                params={'label': label},
                identifiers={
                    'source_table': Form460FilingVersion._meta.db_table,
                    'source_column': f.column,
                }
            )

    def _load_from_form460_schedule_summary_field(self, model, label, field_name):
        """
        Load OCD FilingActionSummaryAmount with from a schedule summary field.
        """
        field = model._meta.get_field(field_name)
        logger.info(' ...%s...' % label)
        execute_custom_sql(
            'insert_filing_action_summary_amounts',
            params={'label': label},
            identifiers={
                'source_table': model._meta.db_table,
                'source_column': field.column,
            }
        )

    def load_form460_data(self):
        """
        Load OCD FilingActionSummaryAmount with data from all Form460 related models.
        """
        logger.info(' Inserting new Filing Action Summary Amounts...')
        logger.info(' ...from Form 460 Summary Sheet...')
        self._load_form460_summary_sheet_data()

        # logger.info(' ...from Form 460 Schedule A Summary...')
        # self._load_from_form460_schedule_summary_field(
        #     Form460ScheduleASummaryVersion,
        #     'Itemized Monetary Contributions',
        #     'itemized_contributions',
        # )
        # self._load_from_form460_schedule_summary_field(
        #     Form460ScheduleASummaryVersion,
        #     'Unitemized Monetary Contributions',
        #     'unitemized_contributions',
        # )

        # logger.info(' ...from Form 460 Schedule C Summary...')
        # self._load_from_form460_schedule_summary_field(
        #     Form460ScheduleCSummaryVersion,
        #     'Itemized Non-monetary Contributions',
        #     'itemized_contributions',
        # )
        # self._load_from_form460_schedule_summary_field(
        #     Form460ScheduleCSummaryVersion,
        #     'Unitemized Non-monetary Contributions',
        #     'unitemized_contributions',
        # )


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
