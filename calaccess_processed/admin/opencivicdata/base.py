#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for OpenCivicData base models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.Division)
class DivisionAdmin(BaseAdmin):
    """
    Custom admin for the Division model.
    """
    list_display = (
        'name',
        'subtype1',
        'subtype2',
    )
    search_fields = ('name',)
    list_filter = (
        'subtype1',
        'subtype2',
    )


@admin.register(models.Organization)
class OrganizationAdmin(BaseAdmin):
    """
    Custom admin for the Organization model.
    """
    list_display = (
        'name',
        'parent',
        'jurisdiction',
        'classification'
    )
    search_fields = ('name',)
    list_filter = (
        'classification',
    )
