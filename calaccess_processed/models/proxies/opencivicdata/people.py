#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from django.db import models
from opencivicdata.core.models import Person


class OCDPersonManager(models.Manager):
    """
    A custom manager for working with the OCD Person model.
    """
    def get_by_filer_id(self, filer_id):
        """
        Returns a Person object linked to a CAL-ACCESS filer_id, if it exists.
        """
        return self.get_queryset().get(
            identifiers__scheme='calaccess_filer_id',
            identifiers__identifier=filer_id,
        )


class OCDPersonProxy(Person):
    """
    A proxy on the OCD Person model with helper methods.
    """
    objects = OCDPersonManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True

    def update_name(self):
        """
        Update name field to the latest candidate record.
        """
        # Get the latest candidate name
        latest_candidate_name = self.candidacies.latest('contest__election__date').candidate_name
        # If the latest candidate name doesn't match the current name
        if self.name != latest_candidate_name:
            # Move the current name into other_names
            if not self.other_names.filter(name=self.name).exists():
                self.other_names.create(name=self.name)
            # Reset the main one
            self.name = latest_candidate_name
            # Save out.
            self.save()

    def add_other_name(self, name, note):
        """
        If an alternative name is not available, add it to the metadata.
        """
        # If the provided name is the default name, just quit.
        if name == self.name:
            return False

        # If the other name has already been logged, quit.
        exists = self.other_names.filter(name=name).exists()
        if exists:
            return False

        # If we've made it this far, it's time to add
        self.other_names.create(name=name, note=note)
        return True

    def add_filer_id(self, filer_id):
        """
        Adds the provided CAL-ACCESS filer_id to the object metadata.
        """
        kwargs = dict(
            scheme="calaccess_filer_id",
            identifier=filer_id
        )
        # If it already exists, quit out.
        if self.identifiers.filter(**kwargs).count():
            return False
        # Otherwise add it.
        self.identifiers.create(**kwargs)
        return True
