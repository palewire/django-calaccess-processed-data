#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db import models
from opencivicdata.core.models import Division
from .base import OCDProxyModelMixin
from postgres_copy import CopyQuerySet


class OCDAssemblyDivisionManager(models.Manager):
    """
    Custom manager for state assembly OCD Divisions.
    """
    def get_queryset(self):
        """
        Filters down to state assembly divisions.
        """
        return super(OCDAssemblyDivisionManager, self).get_queryset().filter(
            subid1='ca',
            subtype2='sldl',
        )


class OCDSenateDivisionManager(models.Manager):
    """
    Custom manager for state senate OCD Divisions.
    """
    def get_queryset(self):
        """
        Filters down to state senate divisions.
        """
        return super(OCDSenateDivisionManager, self).get_queryset().filter(
            subid1='ca',
            subtype2='sldu',
        )


class OCDCaliforniaDivisionManager(models.Manager):
    """
    Custom manager for OCD Divisions in California.
    """
    def get_queryset(self):
        """
        Filters down to divisions in California.
        """
        return super(OCDCaliforniaDivisionManager, self).get_queryset().filter(
            subid1='ca',
        )

    def california(self):
        """
        Returns state of California division.
        """
        return super(OCDCaliforniaDivisionManager, self).get_queryset().get(
            id='ocd-division/country:us/state:ca'
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
