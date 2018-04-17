#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals

# Models
from calaccess_processed.proxies import OCDProxyModelMixin
from opencivicdata.core.models import Person, PersonIdentifier, PersonName

# Managers
from calaccess_processed.managers import BulkLoadSQLManager
from calaccess_processed_elections.managers import OCDPersonManager


class OCDPersonProxy(Person, OCDProxyModelMixin):
    """
    A proxy on the OCD Person model with helper methods.
    """
    objects = OCDPersonManager()

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
        app_label = "calaccess_processed_elections"
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
        from calaccess_processed_elections.proxies import ScrapedCandidateProxy
        filer_ids = [i.identifier for i in self.identifiers.filter(scheme="calaccess_filer_id")]
        return ScrapedCandidateProxy.objects.filter(scraped_id__in=filer_ids).order_by("-election")

    @property
    def form501s(self):
        """
        Returns any linked Form 501s filings.
        """
        from calaccess_processed_elections.proxies import OCDCandidacyProxy
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
    objects = BulkLoadSQLManager()

    class Meta:
        """
        Make this a proxy model.
        """
        app_label = "calaccess_processed_elections"
        proxy = True


class OCDPersonNameProxy(PersonName, OCDProxyModelMixin):
    """
    A proxy on the OCD PersonName model with helper methods.
    """
    objects = BulkLoadSQLManager()

    class Meta:
        """
        Make this a proxy model.
        """
        app_label = "calaccess_processed_elections"
        proxy = True
