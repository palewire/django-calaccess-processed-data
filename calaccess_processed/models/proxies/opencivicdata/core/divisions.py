#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals

# Models
from ..base import OCDProxyModelMixin
from opencivicdata.core.models import Division

# Managers
from postgres_copy import CopyQuerySet
from calaccess_processed.managers import (
    OCDAssemblyDivisionManager,
    OCDSenateDivisionManager,
    OCDCaliforniaDivisionManager
)


class OCDDivisionProxy(Division, OCDProxyModelMixin):
    """
    A proxy on the OCD Division model with helper methods.
    """
    objects = OCDCaliforniaDivisionManager.from_queryset(CopyQuerySet)()
    assembly = OCDAssemblyDivisionManager()
    senate = OCDSenateDivisionManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
