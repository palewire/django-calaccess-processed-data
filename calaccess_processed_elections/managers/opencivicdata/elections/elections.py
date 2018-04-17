#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom managers for the OCD Election model.
"""
from __future__ import unicode_literals
from calaccess_processed.managers import BulkLoadSQLManager


class OCDPartisanPrimaryManager(BulkLoadSQLManager):
    """
    Custom manager for limiting OCD elections querysets to partisan primaries.
    """
    def get_queryset(self):
        """
        Returns whether or not this was a primary election held in the partisan era prior to 2012.
        """
        return super(OCDPartisanPrimaryManager, self).get_queryset().filter(
            date__year__lt=2012,
            name__icontains='PRIMARY'
        )


class OCDElectionManager(BulkLoadSQLManager):
    """
    Custom helpers for the OCD Election model.
    """
    def create_from_calaccess(self, name, dt, election_id=None, election_type=None):
        """
        Create an OCD Election object.
        """
        from calaccess_processed_elections.proxies import OCDOrganizationProxy, OCDDivisionProxy

        # Create the object
        obj = self.get_queryset().create(
            name=name,
            date=dt,
            administrative_organization=OCDOrganizationProxy.objects.elections_division(),
            division=OCDDivisionProxy.objects.california(),
        )

        # And add the identifier so we can find it in the future
        if election_id:
            obj.identifiers.create(scheme='calaccess_election_id', identifier=election_id)

        # Add the election type so we can pull it out later if we want it.
        if election_type:
            obj.extras['calaccess_election_type'] = [election_type]
            obj.save()

        # Pass it back
        return obj
