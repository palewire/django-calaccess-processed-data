#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom manager for the Jurisdiction model.
"""
from __future__ import unicode_literals
from django.apps import apps
from postgres_copy import CopyManager


class OCDJurisdictionManager(CopyManager):
    """
    Custom helpers for the OCD Jurisdiction model.
    """
    def california(self):
        """
        Returns California State Government jurisdiction.
        """
        OCDDivisionProxy = apps.get_model("calaccess_processed", "OCDDivisionProxy")
        qs = self.get_queryset()
        division = OCDDivisionProxy.objects.california()
        return qs.get_or_create(name='California', classification='government', division=division)[0]
