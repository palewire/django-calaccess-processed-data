#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom managers for working with CAL-ACCESS processed data models.
"""
from __future__ import unicode_literals
import os
from django.db import connection
from postgres_copy import CopyManager


class ProcessedDataManager(CopyManager):
    """
    Utilities for loading raw CAL-ACCESS data into processed data models.
    """
    def add_constraints_and_indexes(self):
        """
        Re-create constraints and indexes on the model and its fields.
        """
        with connection.schema_editor() as schema_editor:
            schema_editor.alter_unique_together(
                self.model,
                (),
                self.model._meta.unique_together,
            )

            schema_editor.alter_index_together(
                self.model,
                (),
                self.model._meta.index_together,
            )

            for field in self.model.objects.constrained_fields:
                field_copy = field.__copy__()
                field_copy.db_constraint = False
                schema_editor.alter_field(
                    self.model, field_copy, field
                )

            for field in self.model.objects.indexed_fields:
                field_copy = field.__copy__()
                field_copy.db_index = False
                schema_editor.alter_field(
                    self.model, field_copy, field
                )

    def drop_constraints_and_indexes(self):
        """
        Temporarily drop constraints and indexes on the model and its fields.
        """
        with connection.schema_editor() as schema_editor:
            schema_editor.alter_unique_together(
                self.model,
                self.model._meta.unique_together,
                (),
            )

            schema_editor.alter_index_together(
                self.model,
                self.model._meta.index_together,
                (),
            )

            for field in self.model.objects.constrained_fields:
                field_copy = field.__copy__()
                field_copy.db_constraint = False
                schema_editor.alter_field(
                    self.model, field, field_copy
                )

            for field in self.model.objects.indexed_fields:
                field_copy = field.__copy__()
                field_copy.db_index = False
                schema_editor.alter_field(
                    self.model, field, field_copy
                )

    def load_raw_data(self):
        """
        Load the model by executing its raw sql load query.

        Temporarily drops any constraints or indexes on the model.
        """
        try:
            self.drop_constraints_and_indexes()
        except ValueError as e:
            print(e)
            print('Constrained fields: %s' % self.constrained_fields)
            print('Indexed fields: %s' % self.indexed_fields)
            dropped = False
        else:
            dropped = True

        c = connection.cursor()
        try:
            c.execute(self.raw_data_load_query)
        finally:
            c.close()
            if dropped:
                self.add_constraints_and_indexes()

    @property
    def constrained_fields(self):
        """
        Returns list of model's fields with db_constraint set to True.
        """
        return [
            f for f in self.model._meta.fields
            if hasattr(f, 'db_constraint') and f.db_constraint
        ]

    @property
    def indexed_fields(self):
        """
        Returns list of model's fields with db_index set to True.
        """
        return [
            f for f in self.model._meta.fields if f.db_index
        ]

    @property
    def has_raw_data_load_query(self):
        """
        Return true if the model has a .sql load query file.
        """
        if os.path.exists(self.raw_data_load_query_path):
            return True
        else:
            return False

    @property
    def db_table(self):
        """
        Return the model's database table name as a string.
        """
        return self._meta.db_table

    @property
    def raw_data_load_query(self):
        """
        Return string of raw sql for loading the model.
        """
        sql = ''
        if self.has_raw_data_load_query:
            with open(self.raw_data_load_query_path) as f:
                sql = f.read()
        return sql

    @property
    def raw_data_load_query_path(self):
        """
        Return the path to the .sql file with the model's loading query.
        """
        return os.path.join(
            os.path.dirname(__file__),
            'sql',
            'load_%s_model.sql' % self.model._meta.model_name,
        )
