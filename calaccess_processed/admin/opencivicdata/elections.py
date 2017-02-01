#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for OpenCivicData campaign models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.Election)
class ElectionAdmin(BaseAdmin):
    """
    Custom admin for the Election model.
    """
    list_display = (
        'name',
        'start_time',
        'administrative_org',
        'is_statewide'
    )
    search_fields = ('name',)
    date_hierarchy = 'start_time'


@admin.register(models.Party)
class PartyAdmin(BaseAdmin):
    """
    Custom admin for the Party model.
    """
    list_display = (
        'name',
        'abbreviation',
        'color',
    )
    search_fields = ('name',)
