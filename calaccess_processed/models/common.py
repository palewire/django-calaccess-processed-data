#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing general filer and filing data derived from raw CAL-ACCESS data.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.managers import ProcessedDataManager


@python_2_unicode_compatible
class FilerIDValue(models.Model):
    """
    Every unique filer_id in the CAL-ACCESS database.

    Includes the table and column in which the unique value was observed
    """
    table_name = models.CharField(
        verbose_name="table_name",
        max_length=30,
        db_index=True,
        null=False,
        blank=False,
        help_text="Name of the database table with the column where the "
                  "filer_id value was observed.",
    )
    column_name = models.CharField(
        verbose_name="column_name",
        max_length=20,
        null=False,
        blank=False,
        db_index=True,
        help_text="Name of the database column where the filer_id value was "
                  "observed.",
    )
    value = models.CharField(
        verbose_name="filer_id value",
        max_length=15,
        null=False,
        blank=False,
        db_index=True,
        help_text="Unique filer_id value in the given database table and column.",
    )
    occur_count = models.IntegerField(
        verbose_name="occurence count",
        null=False,
        db_index=True,
        help_text="Count of occurences of the filer_id value in the given "
                  "database table and column.",
    )

    objects = ProcessedDataManager()

    class Meta:
        """
        Meta model options.
        """
        app_label = 'calaccess_processed'

    def __str__(self):
        return str(self.value)
