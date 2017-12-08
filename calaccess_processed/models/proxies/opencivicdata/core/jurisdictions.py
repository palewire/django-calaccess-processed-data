#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from opencivicdata.core.models import Jurisdiction
from postgres_copy import CopyManager
from .divisions import OCDDivisionProxy
from ..base import OCDProxyModelMixin


class OCDJurisdictionManager(CopyManager):
    """
    Custom helpers for the OCD Jurisdiction model.
    """
    def california(self):
        """
        Returns California State Government jurisdiction.
        """
        return self.get_queryset().get_or_create(
            name='California',
            classification='government',
            division=OCDDivisionProxy.objects.california(),
        )[0]


class OCDJurisdictionProxy(Jurisdiction, OCDProxyModelMixin):
    """
    A proxy on the OCD Jurisdiction model with helper methods.
    """
    objects = OCDJurisdictionManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
