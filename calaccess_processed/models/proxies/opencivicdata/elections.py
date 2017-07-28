#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db import models
from .divisions import OCDDivisionProxy
from django.utils.text import get_text_list
from .organizations import OCDOrganizationProxy
from opencivicdata.elections.models import Election


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
        if election_id:
            obj.identifiers.create(scheme='calaccess_election_id', identifier=election_id)

        # Add the election type so we can pull it out later if we want it.
        if election_type:
            obj.extras['calaccess_election_type'] = [election_type]
            obj.save()

        # Pass it back
        return obj


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

    def add_election_type(self, election_type):
        """
        Add election_type to 'calaccess_election_type' in extras field (if missing).
        """
        if 'election_type' in self.extras.keys():
            # and if this one isn't included
            if election_type not in self.extras[
                'calaccess_election_type'
            ]:
                # then append
                self.extras['calaccess_election_type'].append(election_type)
                # and save
                self.save()
        else:
            # if election doesn't already have types, add the key
            self.extras['calaccess_election_type'] = [election_type]
            # and save
            self.save()

        return

    def add_election_id(self, election_id):
        """
        Add election_id to identifiers, if missing.
        """
        if not self.identifiers.filter(
            scheme='calaccess_election_id',
            identifier=election_id,
        ).exists():
            self.identifiers.create(
                scheme='calaccess_election_id',
                identifier=election_id,
            )
            self.save()

        return

    def is_primary(self):
        """
        Returns whether or now the election was a primary.
        """
        return 'PRIMARY' in self.name.upper()

    def is_general(self):
        """
        Returns whether or now the election was a general election.
        """
        return 'GENERAL' in self.name.upper()

    def is_special(self):
        """
        Returns whether or now the election was a special election.
        """
        return 'SPECIAL' in self.name.upper()

    def is_recall(self):
        """
        Returns whether or now the election was a recall.
        """
        return 'RECALL' in self.name.upper()

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

    @property
    def identifier_list(self):
        """
        Returns a prettified list of OCD identifiers.
        """
        template = "{0.scheme}: {0.identifier}"
        return get_text_list([template.format(i) for i in self.identifiers.all()])

    @property
    def source_list(self):
        """
        Returns a prettified list of OCD sources.
        """
        return get_text_list(list(self.sources.all()))
