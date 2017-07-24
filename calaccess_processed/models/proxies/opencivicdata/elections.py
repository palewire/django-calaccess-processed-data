#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db import models
from opencivicdata.elections.models import Election
from .organizations import OCDOrganizationProxy
from .divisions import OCDDivisionProxy


class OCDElectionManager(models.Manager):
    """
    Custom helpers for the OCD Post model.
    """
    def create_with_name_and_date(self, name, dt):
        """
        Create an OCD Election object.
        """
        return self.get_queryset().create(
            name=name,
            date=dt,
            administrative_organization=OCDOrganizationProxy.objects.elections_division(),
            division=OCDDivisionProxy.objects.california(),
        )


class OCDElectionProxy(Election):
    """
    A proxy for the Election model in opencivicdata app.
    """
    objects = OCDElectionManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True

    def is_primary(self):
        """
        Returns whether or now the election was a primary.
        """
        return 'PRIMARY' in self.name.upper()

    def is_partisan_primary(self):
        """
        Returns whether or not this was a priamry election held in the partisan era prior to 2012.
        """
        if self.is_primary():
            if self.date.year < 2012:
                return True
        return False
