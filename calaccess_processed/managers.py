#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom managers for working with CAL-ACCESS processed data models.
"""
from __future__ import unicode_literals
import os
from django.db import models, connection
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.query import Query
from psycopg2.sql import Literal


class SQLCopyToCompiler(SQLCompiler):
    """
    Custom SQL compiler for creating a COPY TO query (postgres backend only).
    """
    def setup_query(self):
        """
        Extend the default SQLCompiler.setup_query to add re-ordering of items in select.
        """
        super(SQLCopyToCompiler, self).setup_query()
        if self.query.copy_to_fields:
            self.select = []
            for field in self.query.copy_to_fields:
                # raises error if field is not available
                expression = self.query.resolve_ref(field)

                if field in self.query.annotations:
                    selection = (expression, self.compile(expression), field)
                else:
                    selection = (expression, self.compile(expression), None)

                self.select.append(selection)

    def execute_sql(self, csv_path):
        """
        Run the COPY TO query.
        """
        # open file for writing
        # use stdout to avoid file permission issues
        with open(csv_path, 'wb') as stdout:
            with connection.cursor() as c:
                # compose SELECT query parameters as sql strings
                params = self.as_sql()[1]
                adapted_params = tuple(
                    Literal(p).as_string(c.cursor) for p in params
                )
                # compile the SELECT query
                select_sql = self.as_sql()[0] % adapted_params
                # then the COPY TO query
                copy_to_sql = "COPY (%s) TO STDOUT CSV HEADER" % select_sql
                # then executw
                c.cursor.copy_expert(copy_to_sql, stdout)
        return


class CopyToQuery(Query):
    """
    Represents a "copy to" SQL query.
    """
    def __init__(self, *args, **kwargs):
        """
        Extend inherited __init__ method to include setting copy_to_fields from args.
        """
        super(CopyToQuery, self).__init__(*args, **kwargs)
        self.copy_to_fields = args

    def get_compiler(self, using=None, connection=None):
        """
        Return a SQLCopyToCompiler object.
        """
        return SQLCopyToCompiler(self, connection, using)


class CopyToQuerySet(models.QuerySet):
    """
    Subclass of QuerySet that adds _copy_to_csv method.
    """
    def copy_to_csv(self, csv_path, *fields):
        """
        Copy current objects in QuerySet to a file at csv_path.

        Use optional fields arguments to specify the names of fields
        to be copied and their order in the csv file.

        Return a call to .execute_sql() on the compiler of the queryset's query.
        """
        query = self.query.clone(CopyToQuery)
        query.copy_to_fields = fields

        return query.get_compiler(
            self.db, connection=connection
        ).execute_sql(csv_path)


class ProcessedDataManager(models.Manager):
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
