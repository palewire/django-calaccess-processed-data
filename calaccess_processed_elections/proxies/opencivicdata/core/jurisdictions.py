#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals

# Models
from calaccess_processed.proxies import OCDProxyModelMixin
from opencivicdata.core.models import Jurisdiction

# Managers
from calaccess_processed_elections.managers import OCDJurisdictionManager


class OCDJurisdictionProxy(Jurisdiction, OCDProxyModelMixin):
    """
    A proxy on the OCD Jurisdiction model with helper methods.
    """
    objects = OCDJurisdictionManager()

    class Meta:
        """
        Make this a proxy model.
        """
        app_label = "calaccess_processed_elections"
        proxy = True
