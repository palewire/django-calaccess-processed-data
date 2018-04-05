#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for more quickly loading bulk data.
"""
from __future__ import unicode_literals
import logging
from django.db import models
from django.db import connection
from postgres_copy.managers import ConstraintQuerySet
logger = logging.getLogger(__name__)


class BulkLoadSQLQuerySet(ConstraintQuerySet):
    """
    Utilities for more quickly loading bulk data into a model with custom SQL.
    """
    def load(self):
        """
        Load the model by executing its corresponding raw SQL query.

        Temporarily drops any constraints or indexes on the model.
        """
        # Drop constraints and indexes to speed loading
        self.drop_constraints()
        self.drop_indexes()

        # Run the actual loader SQL
        self.execute()

        # Restore the constraints and index that were dropped
        self.restore_constraints()
        self.restore_indexes()

    def execute(self):
        """
        Run the loader command.
        """
        with connection.cursor() as c:
            c.execute(self.sql)


BulkLoadSQLManager = models.Manager.from_queryset(BulkLoadSQLQuerySet)
