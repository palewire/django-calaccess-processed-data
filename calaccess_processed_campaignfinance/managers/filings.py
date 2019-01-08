#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for OCD Filing related managers.
"""
from __future__ import unicode_literals
import logging
from psycopg2 import sql
from .base import CampaignFinanceManager
logger = logging.getLogger(__name__)


class OCDFilingManager(CampaignFinanceManager):
    """
    Manager with custom methods for OCD Filing model.
    """
    def _update_filings_from_form460_field(self, target_column, source_column):
        """
        Update target_column on OCD Filing with value from source_column.
        """
        from calaccess_processed_filings.models import Form460Filing, Filing

        source_table_identifier = sql.Identifier(Form460Filing._meta.db_table)
        source_column_identifier = sql.Identifier(Form460Filing._meta.get_field(source_column).column)
        target_column_identifier = sql.Identifier(Filing._meta.get_field(target_column).column)
        self.execute_custom_sql(
            'opencivicdata/campaign_finance/filings/update_filings_from_formfiling_table',
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
        processed_data_table_identifier = sql.Identifier(model._meta.db_table)
        self.execute_custom_sql(
            'opencivicdata/campaign_finance/filings/update_filings_filer_id',
            composables={
                'processed_data_table': processed_data_table_identifier,
            },
        )

    def load(self):
        """
        Load OCD Filing with data extracted from Form460Filing.
        """
        from calaccess_processed_filings.models import Form460Filing

        # Updating existing Filings...
        self._update_filings_from_form460_field('coverage_start_date', 'from_date')
        self._update_filings_from_form460_field('coverage_end_date', 'thru_date')
        self._update_filings_filer_id(Form460Filing)

        # Inserting new Filings...
        self.execute_custom_sql('opencivicdata/campaign_finance/filings/insert_filings_from_form460s')


class OCDFilingIdentifierManager(CampaignFinanceManager):
    """
    Manager with custom methods for OCD FilingIdentifier model.
    """
    def load(self):
        """
        Load OCD FilingIdentifier with data extracted from Form460Filing.
        """
        # Inserting new Filing Identifiers...
        self.execute_custom_sql('opencivicdata/campaign_finance/filings/insert_filing_ids_from_form460s')
        # Removing "calaccess_filing_id" from extras field on Filing...
        self.execute_custom_sql('opencivicdata/campaign_finance/filings/remove_calaccess_filing_ids_from_filings')


class OCDFilingActionManager(CampaignFinanceManager):
    """
    Manager with custom methods for OCD FilingAction model.
    """
    def load(self):
        """
        Load OCD FilingAction with data extracted from Form460FilingVersion.
        """
        # Inserting new Filing Actions...
        self.execute_custom_sql('opencivicdata/campaign_finance/filings/insert_filing_actions_from_form460s')

        # Setting is_current false on actions of amended Filings...
        self.execute_custom_sql('opencivicdata/campaign_finance/filings/set_is_current_for_old_filing_actions')

        # Setting is_current true on latest Filing Actions...
        self.execute_custom_sql('opencivicdata/campaign_finance/filings/set_is_current_for_new_filing_actions')


class OCDFilingActionSummaryAmountManager(CampaignFinanceManager):
    """
    Manager with custom methods for OCD FilingActionSummaryAmount model.
    """
    def _load_form460_summary_sheet_data(self):
        """
        Load OCD FilingActionSummaryAmount with data extracted from Form460FilingVersion.
        """
        from calaccess_processed_filings.models import Form460FilingVersion

        sum_fields = [
            f for f in Form460FilingVersion._meta.get_fields()
            if f.__class__.__name__ == 'IntegerField' and f.name[-3:] != '_id'
        ]
        table_composable = sql.Identifier(Form460FilingVersion._meta.db_table)
        for f in sum_fields:
            label_words = [w.capitalize() for w in f.name.split('_')]
            label = ' '.join(label_words)
            self.execute_custom_sql(
                'opencivicdata/campaign_finance/filings/insert_filing_action_summary_amounts',
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
        source_column_identifier = sql.Identifier(model._meta.get_field(field_name).column)
        self.execute_custom_sql(
            'opencivicdata/campaign_finance/filings/insert_filing_action_summary_amount_from_schedules',
            params={'label': label},
            composables={
                'source_table': source_table_identifier,
                'source_column': source_column_identifier,
            },
        )

    def load(self):
        """
        Load OCD FilingActionSummaryAmount with data from all Form460 related models.
        """
        from calaccess_processed_filings.models import Form460ScheduleASummaryVersion, Form460ScheduleCSummaryVersion

        # Inserting new Filing Action Summary Amounts...
        # ...from Form 460 Summary Sheet...
        self._load_form460_summary_sheet_data()

        # ...from Form 460 Schedule A Summary...
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

        # ...from Form 460 Schedule C Summary...
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
