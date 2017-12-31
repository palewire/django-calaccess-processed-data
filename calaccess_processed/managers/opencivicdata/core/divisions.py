#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom managers for the Division model.
"""
from __future__ import unicode_literals
from django.db import models


class OCDAssemblyDivisionManager(models.Manager):
    """
    Custom manager for state assembly OCD Divisions.
    """
    def get_queryset(self):
        """
        Filters down to state assembly divisions.
        """
        qs = super(OCDAssemblyDivisionManager, self).get_queryset()
        return qs.filter(subid1='ca', subtype2='sldl')


class OCDSenateDivisionManager(models.Manager):
    """
    Custom manager for state senate OCD Divisions.
    """
    def get_queryset(self):
        """
        Filters down to state senate divisions.
        """
        qs = super(OCDSenateDivisionManager, self).get_queryset()
        return qs.filter(subid1='ca', subtype2='sldu')


class OCDCaliforniaDivisionManager(models.Manager):
    """
    Custom manager for OCD Divisions in California.
    """
    def get_queryset(self):
        """
        Filters down to divisions in California.
        """
        qs = super(OCDCaliforniaDivisionManager, self).get_queryset()
        return qs.filter(subid1='ca')

    def california(self):
        """
        Returns state of California division.
        """
        qs = super(OCDCaliforniaDivisionManager, self).get_queryset()
        return qs.get(id='ocd-division/country:us/state:ca')
