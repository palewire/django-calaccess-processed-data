#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom managers for working with CAL-ACCESS processed data models.
"""
from __future__ import unicode_literals
import os
from django.db import models, connection

class ProcessedDataManager(models.Manager):
    """
    Utilities for loading raw CAL-ACCESS data into processed data models.
    """
    def load_raw_data(self):
        with connection.cursor() as c:
            c.execute(self.raw_data_load_query)

    @property
    def raw_data_load_query_path(self):
        return os.path.join(
            os.path.dirname(__file__),
            'sql',
            'load_%s_model.sql' % self.model._meta.model_name,
        )
    
    @property
    def has_raw_data_load_query(self):
        if os.path.exists(self.raw_data_load_query_path):
            return True
        else:
            return False    

    @property
    def raw_data_load_query(self):
        sql = ''
        if self.has_raw_data_load_query:
            with open(self.raw_data_load_query_path) as f:
                sql = f.read()
        return sql

    @property
    def db_table(self):
        """
        Return the model's database table name as a string.
        """
        return self._meta.db_table

