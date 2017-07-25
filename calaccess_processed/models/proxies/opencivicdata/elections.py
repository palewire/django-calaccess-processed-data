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
    def create_from_calaccess(self, name, dt, election_id=None, election_type=None):
        """
        Create an OCD Election object.
        """
        # Create the object
        obj = self.get_queryset().create(
            name=name,
            date=dt,
            administrative_organization=OCDOrganizationProxy.objects.elections_division(),
            division=OCDDivisionProxy.objects.california(),
        )

        # And add the identifier so we can find it in the future
        if calaccess_election_id:
            obj.identifiers.create(scheme='calaccess_election_id', identifier=calaccess_election_id)

        # Add the election type so we can pull it out later if we want it.
        if election_type:
            obj.extras['calaccess_election_type'] = election_type
            obj.save()



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

    @property
    def election_type(self):
        """
        Returns the CAL-ACCESS election type if it's been included with this record.
        """
        return self.extras.get('calaccess_election_type', None)
