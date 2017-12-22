#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom SQL scripts and helper functions for executing them.
"""
import os
import re
import logging
from psycopg2 import sql
from django.db import connection
logger = logging.getLogger(__name__)


def get_custom_sql_path(file_name):
    """
    Return the full path with extenstion to file_name.
    """
    return os.path.join(os.path.dirname(__file__), '%s.sql' % file_name)


def get_custom_sql_str(file_path):
    """
    Return the custom sql_str in file_path.
    """
    with open(file_path, 'r') as f:
        sql_str = f.read()
    return sql_str


def compose_custom_sql(sql_str, **kwargs):
    """
    Return a psycopg2.sql Composable.
    """
    return sql.SQL(sql_str).format(**kwargs)


def extract_operation_from_sql(sql_str):
    """
    Return the operation (as a string) declared in the SQL string.
    """
    match = re.search(r'^([A-z]+)', sql_str, re.M)
    if match:
        past_tense = re.sub(r'E$', '', match.group())
        operation = '%sed' % past_tense.lower()
    else:
        operation = 'affected'
    return operation


def log_row_count(row_count, operation):
    """
    Log the number of rows and the operation performed.
    """
    if row_count == 1:
        string = ' %s row %s.' % (row_count, operation)
    else:
        string = ' %s rows %s.' % (row_count, operation)
    logger.info(string)


def execute_custom_sql(file_name, params=None, composables=None):
    """
    Execute custom sql.

    Args:
        file_name (str): Name of .sql file.
        params (dict): Map of named placeholder in sql to parameter.
        composables (dict): Map of named placeholder in sql to psycopg2 sql Composable.

    Log the number of rows and operation performed.
    """
    file_path = get_custom_sql_path(file_name)
    sql_str = get_custom_sql_str(file_path)
    operation = extract_operation_from_sql(sql_str)
    if composables:
        composed_sql = compose_custom_sql(sql_str, **composables)
    else:
        composed_sql = sql_str
    with connection.cursor() as cursor:
        cursor.execute(composed_sql, params)
        log_row_count(cursor.rowcount, operation)
