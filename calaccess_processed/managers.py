#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for more quickly loading bulk data.
"""
from __future__ import unicode_literals

# Database stuff
from django.db import connection
from postgres_copy.managers import CopyManager

# Logging
import logging
logger = logging.getLogger(__name__)


class BulkLoadSQLManager(CopyManager):
    """
    Utilities for more quickly loading bulk data into a model with custom SQL.
    """
    app_name = "calaccess_processed"

    def get_sql(self):
        """
        Return string of raw sql for loading the model.
        """
        raise NotImplementedError

    def get_sql_path(self, file_name):
        """
        Return the full path with extenstion to file_name.
        """
        sql_path = apps.get_app_config(self.app_name).sql_directory_path
        return os.path.join(sql_path, '%s.sql' % file_name)
