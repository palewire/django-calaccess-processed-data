#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db import models
from opencivicdata.core.models import (
    Person,
    PersonIdentifier,
    PersonName,
)
from postgres_copy import CopyQuerySet
from .base import OCDProxyModelMixin


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


class OCDPersonProxy(Person, OCDProxyModelMixin):
    """
    A proxy on the OCD Person model with helper methods.
    """
    objects = OCDPersonManager.from_queryset(CopyQuerySet)()

    copy_to_fields = (
        ('id',),
        ('name',),
        ('sort_name',),
        ('family_name',),
        ('given_name',),
        ('image',),
        ('gender',),
        ('summary',),
        ('national_identity',),
        ('biography',),
        ('birth_date',),
        ('death_date',),
        ('created_at',),
        ('updated_at',),
        ('extras',),
        ('locked_fields',),
    )

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
        Add name to Person's list of other names along with note.

        If name was previously added to person, append note to existing note.

        Return boolean value indicating if the name was created or not.
        """
        # If the provided name is the default name, just quit.
        if name == self.name:
            created = False
        elif self.other_names.filter(name=name).exists():
            created = False
            # append the note, if not already there
            existing_name = self.other_names.get(name=name)
            if note not in existing_name.note:
                existing_name.note = '{0}, {1}'.format(existing_name.note, note)
        else:
            created = True
            self.other_names.create(name=name, note=note)
        return created

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

    @property
    def filer_id(self):
        """
        Returns the CAL-ACCESS filer_id linked with the object, if any.
        """
        return self.identifiers.get(scheme="calaccess_filer_id")

    @property
    def scraped_candidates(self):
        """
        Returns the scraped candidates linked to this candidacy.
        """
        from calaccess_processed.models import ScrapedCandidateProxy
        filer_ids = [i.identifier for i in self.identifiers.filter(scheme="calaccess_filer_id")]
        return ScrapedCandidateProxy.objects.filter(scraped_id__in=filer_ids).order_by("-election")

    @property
    def form501s(self):
        """
        Returns any linked Form 501s filings.
        """
        from calaccess_processed.models import OCDCandidacyProxy
        candidacies = OCDCandidacyProxy.objects.filter(person=self)
        form501s = []
        for c in candidacies:
            for f in c.form501s:
                if f not in form501s:
                    form501s.append(f)
        return form501s


class OCDPersonIdentifierProxy(PersonIdentifier, OCDProxyModelMixin):
    """
    A proxy on the OCD PersonIdentifier model.
    """
    objects = CopyQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDPersonNameProxy(PersonName, OCDProxyModelMixin):
    """
    A proxy on the OCD PersonName model with helper methods.
    """
    objects = CopyQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
