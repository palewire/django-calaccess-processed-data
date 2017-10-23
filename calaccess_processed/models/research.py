#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing general filer and filing data derived from raw CAL-ACCESS data for research of the system.
"""
from __future__ import unicode_literals
from django.db import models
from calaccess_processed.models import CalAccessBaseModel
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class FilerIDValue(CalAccessBaseModel):
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

    class Meta:
        """
        Meta model options.
        """
        app_label = 'calaccess_processed'
        verbose_name = "Filer ID value"
        unique_together = (('table_name', 'column_name', 'value'),)

    def __str__(self):
        return str(self.value)


@python_2_unicode_compatible
class FilingIDValue(CalAccessBaseModel):
    """
    Every unique filing_id in the CAL-ACCESS database.

    Includes the table and column in which the unique value was observed
    """
    table_name = models.CharField(
        verbose_name="table_name",
        max_length=30,
        null=False,
        blank=False,
        db_index=True,
        help_text="Name of the database table with the column where the "
                  "filing_id value was observed.",
    )
    value = models.IntegerField(
        verbose_name="filing_id value",
        null=False,
        blank=False,
        db_index=True,
        help_text="Unique filing_id value in the given database table and column.",
    )
    occur_count = models.IntegerField(
        verbose_name="occurence count",
        null=False,
        db_index=True,
        help_text="Count of occurences of the filing_id value in the given "
                  "database table and column.",
    )

    class Meta:
        """
        Meta model options.
        """
        app_label = 'calaccess_processed'
        verbose_name = "Filing ID value"
        unique_together = (('table_name', 'value'),)

    def __str__(self):
        return str(self.value)
