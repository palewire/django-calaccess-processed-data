#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom manager for the OCD Person model.
"""
from __future__ import unicode_literals
from calaccess_processed.managers import BulkLoadSQLManager


class OCDPersonManager(BulkLoadSQLManager):
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
