#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals, absolute_import
from calaccess_raw.models import FilerToFilerTypeCd
from calaccess_processed_elections.managers import RawFilerToFilerTypeCdManager


class RawFilerToFilerTypeCdProxy(FilerToFilerTypeCd):
    """
    Proxy model with extra tools for working with the calaccess_raw FilerToFilerTypeCd model.
    """
    objects = RawFilerToFilerTypeCdManager()

    class Meta:
        """
        Make this a proxy model.
        """
        app_label = "calaccess_processed_elections"
        proxy = True
