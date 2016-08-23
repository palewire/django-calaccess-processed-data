#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for tracking models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.ProcessedDataVersion)
class ProcessedDataVersionAdmin(BaseAdmin):
    """
    Custom admin for the ProcessedDataVersion model.
    """
    list_display = (
        "id",
        "raw_version",
        "process_start_datetime",
        "process_finish_datetime",
        "pretty_zip_size",
    )
    list_display_links = ('process_start_datetime',)
    list_filter = ("process_finish_datetime",)


@admin.register(models.ProcessedDataFile)
class ProcessedDataFileAdmin(BaseAdmin):
    """
    Custom admin for the ProcessedDataFile model.
    """
    list_display = (
        "id",
        "version",
        "file_name",
        "records_count",
    )
    list_display_links = ('id', 'file_name',)
    list_filter = ("version__process_start_datetime",)
