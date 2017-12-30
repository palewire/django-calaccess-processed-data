#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom manager for loading raw data in to "filings" models.
"""
from __future__ import unicode_literals
import logging
from django.db import connection
from .constraints import ConstraintsManager
from calaccess_processed.sql import get_custom_sql_path
logger = logging.getLogger(__name__)


class FilingsManager(ConstraintsManager):
    """
    Utilities for more quickly loading bulk data.
    """
    def load(self):
        """
        Load the model by executing its raw sql load query.

        Temporarily drops any constraints or indexes on the model.
        """
        self.drop_constraints_and_indexes()
        with connection.cursor() as c:
            c.execute(self.custom_sql)
        self.add_constraints_and_indexes()

    @property
    def custom_sql(self):
        """
        Return string of raw sql for loading the model.
        """
        return open(self.custom_sql_path, 'r').read()

    @property
    def custom_sql_path(self):
        """
        Return the path to the .sql file with the model's loading query.
        """
        file_name = 'filings/load_%s_model' % self.model._meta.model_name
        return get_custom_sql_path(file_name)
