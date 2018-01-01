#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base proxy model for OCD campaign_finance related managers.
"""
from __future__ import unicode_literals
from django.apps import apps

# Database
from psycopg2 import sql
from django.db import connection

# Managers
from postgres_copy import CopyManager
from calaccess_processed.managers.bulkloadsql import BulkLoadSQLManager

# Text
import re
import os
from django.template.defaultfilters import pluralize

# Logging
import logging
logger = logging.getLogger(__name__)


class BaseOCDBulkLoadSQLManager(BulkLoadSQLManager, CopyManager):
    """
    Base proxy model for OCD campaign_finance related managers.
    """
    def get_sql_path(self, file_name):
        """
        Return the full path with extenstion to file_name.
        """
        return os.path.join(
            apps.get_app_config("calaccess_processed").sql_directory_path,
            '%s.sql' % file_name
        )

    def extract_operation_from_sql(self, sql_str):
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
        file_path = self.get_sql_path(file_name)
        logger.debug("Executing {}".format(file_path))

        # Read in the SQL
        sql_str = open(file_path, 'r').read()

        # Compile it with any composable variables that need to be mixed in.
        if composables:
            composed_sql = sql.SQL(sql_str).format(**composables)
        else:
            composed_sql = sql_str

        # Open a database connection
        with connection.cursor() as cursor:
            # Run the SQL
            cursor.execute(composed_sql, params)

            # Log the result
            operation = self.extract_operation_from_sql(sql_str)
            row_count = cursor.rowcount
            logger.debug('{} {} {}'.format(
                row_count,
                "row" + pluralize(row_count),
                operation
            ))
