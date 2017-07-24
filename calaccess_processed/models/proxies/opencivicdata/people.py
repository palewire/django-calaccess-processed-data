#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
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

    def get_or_create_from_calaccess(self, candidate_name_dict, candidate_filer_id=None):
        """
        Create a Person object using data from the CAL-ACCESS database and scrape.

        If a filer_id is provided, first attempt to lookup the Person by filer_id.
        If matched, and the provided name doesn't match the current name of the Person
        and isn't included in the other names of the Person, add it as an other_name.

        If the person doesn't exist (or the filer_id is not provided), create a
        new Person.

        Returns a tuple (Person object, created), where created is a boolean
        specifying whether a Person was created.
        """
        # If there is a filer_id, try to go that way
        if candidate_filer_id:
            try:
                person = self.get_by_filer_id(candidate_filer_id)
            except self.model.DoesNotExist:
                pass
            else:
                # If we find a match, make sure it has this name variation logged
                person.add_other_name(candidate_name_dict['name'], 'Matched on calaccess_filer_id')
                # Then pass it out.
                return person, False

        # Otherwise create a new one
        person, person_created = self.get_or_create(**candidate_name_dict)

        # If there's a filer_id, add it on
        if candidate_filer_id:
            person.add_filer_id(candidate_filer_id)

        # Pass it back
        return person, person_created


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
