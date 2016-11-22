#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for campaign models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.FilerIDValue)
class FilerIDValueAdmin(BaseAdmin):
    """
    Custom admin for the FilerIDValue model.
    """
    list_display = (
        "table_name",
        "column_name",
        "value",
        "occur_count",
    )
