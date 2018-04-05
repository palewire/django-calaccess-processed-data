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


class BulkLoadSQLManager(models.Manager):
    """
    Utilities for more quickly loading bulk data into a model with custom SQL.
    """
    def get_queryset(self):
        """
        A custom queryset with extra options.
        """
        return ConstraintQuerySet(self.model, using=self._db)

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
