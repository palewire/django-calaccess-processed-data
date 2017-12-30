#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from calaccess_raw.models import FilerToFilerTypeCd
from calaccess_processed.managers import RawFilerToFilerTypeCdManager


class RawFilerToFilerTypeCdProxy(FilerToFilerTypeCd):
    """
    Proxy model with extra tools for working with the calaccess_raw FilerToFilerTypeCd model.
    """
    objects = RawFilerToFilerTypeCdManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
