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
    def load(self):
        """
        Load the model by executing its corresponding raw SQL query.

        Temporarily drops any constraints or indexes on the model.
        """
        # Drop constraints and indexes to speed loading
        self.get_queryset().drop_constraints()
        self.get_queryset().drop_indexes()

        # Run the actual loader SQL
        self.execute()

        # Restore the constraints and index that were dropped
        self.get_queryset().restore_constraints()
        self.get_queryset().restore_indexes()

    def execute(self):
        """
        Run the loader command.
        """
        with connection.cursor() as c:
            c.execute(self.sql)
