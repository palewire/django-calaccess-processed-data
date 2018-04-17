#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom manager for the Jurisdiction model.
"""
from __future__ import unicode_literals
from calaccess_processed.managers import BulkLoadSQLManager


class OCDJurisdictionManager(BulkLoadSQLManager):
    """
    Custom helpers for the OCD Jurisdiction model.
    """
    def california(self):
        """
        Returns California State Government jurisdiction.
        """
        from calaccess_processed_elections.proxies import OCDDivisionProxy
        qs = self.get_queryset()
        division = OCDDivisionProxy.objects.california()
        return qs.get_or_create(name='California', classification='government', division=division)[0]
