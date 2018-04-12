#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base proxy model for OCD campaign_finance related managers.
"""
from __future__ import unicode_literals

# Database
from psycopg2 import sql
from django.db import connection

# Managers
from calaccess_processed.managers import BulkLoadSQLManager

# Text
import re
from django.template.defaultfilters import pluralize

# Logging
import logging
logger = logging.getLogger(__name__)


class CampaignFinanceManager(BulkLoadSQLManager):
    """
    Base proxy model for OCD campaign_finance related managers.
    """
    app_name = "calaccess_processed_campaignfinance"

    def get_sql(self, file_name):
        """
        Return string of raw sql for loading the model.
        """
        sql_path = self.get_sql_path(file_name)
        return open(sql_path, 'r').read()

    def _extract_operation_from_sql(self, sql_str):
        """
        Return the operation (as a string) declared in the SQL string.
        """
        match = re.search(r'^([A-z]+)', sql_str, re.M)
        if match:
            past_tense = re.sub(r'E$', '', match.group())
            return '%sed' % past_tense.lower()
        else:
            return 'affected'

    def execute_custom_sql(self, file_name, params=None, composables=None):
        """
        Execute custom sql.

        Args:
            file_name (str): Name of .sql file.
            params (dict): Map of named placeholder in sql to parameter.
            composables (dict): Map of named placeholder in sql to psycopg2 sql Composable.

        Log the number of rows and operation performed.
        """
        # Get the path to the SQL file
        raw_sql = self.get_sql(file_name)

        # Compile with any composable variables
        if composables:
            composed_sql = sql.SQL(raw_sql).format(**composables)
        else:
            composed_sql = raw_sql

        # Open a database connection
        with connection.cursor() as cursor:
            # Run the SQL
            cursor.execute(composed_sql, params)
            # Get the row row_count
            row_count = cursor.rowcount

        # Log the result
        operation = self._extract_operation_from_sql(raw_sql)
        logger.debug('{} {} {}'.format(
            row_count,
            "row" + pluralize(row_count),
            operation
        ))
