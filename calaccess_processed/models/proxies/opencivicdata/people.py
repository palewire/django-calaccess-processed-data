#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db import models
from django.db.models import Count
from opencivicdata.merge import merge
from opencivicdata.core.models import (
    Person,
    PersonIdentifier,
    PersonName,
)
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

    def merge(self, persons):
        """
        Merge items in persons iterable into one Person object.

        Return the merged Person object.
        """
        # each person will be merged into this one
        keep = persons.pop(0)

        # loop over all the rest
        for i in persons:
            merge(keep, i)
            keep.refresh_from_db()

        # also delete the now duplicated PersonIdentifier objects
        keep_filer_ids = keep.identifiers.filter(scheme='calaccess_filer_id')

        dupe_filer_ids = keep_filer_ids.values("identifier").annotate(
            row_count=Count('id'),
        ).order_by().filter(row_count__gt=1)

        for i in dupe_filer_ids.all():
            # delete all rows with that filer_id
            keep_filer_ids.filter(identifier=i['identifier']).delete()
            # then re-add the one
            keep.identifiers.create(
                scheme='calaccess_filer_id',
                identifier=i['identifier'],
            )

        # and dedupe candidacy records
        # first, make groups by contests with more than one candidacy
        contest_group_q = keep.candidacies.values("contest").annotate(
            row_count=Count('id')
        ).filter(row_count__gt=1)

        # loop over each contest group
        for group in contest_group_q.all():
            cands = keep.candidacies.filter(contest=group['contest'])
            # preference to "qualified" candidacy (from scrape)
            if cands.filter(registration_status='qualified').exists():
                cand_to_keep = cands.filter(registration_status='qualified').all()[0]
            # or the one with the most recent filed_date
            else:
                cand_to_keep = cands.latest('filed_date')

            # loop over all the other candidacies in the group
            for cand_to_discard in cands.exclude(id=cand_to_keep.id).all():
                # assuming the only thing in extras is form501_filing_ids
                if 'form501_filing_ids' in cand_to_discard.extras:
                    for i in cand_to_discard.extras['form501_filing_ids']:
                        self.link_form501_to_candidacy(i, cand_to_keep)
                cand_to_keep.refresh_from_db()

                if 'form501_filing_ids' in cand_to_keep.extras:
                    self.update_candidacy_from_form501s(cand_to_keep)
                cand_to_keep.refresh_from_db()

                # keep the candidate_name, if not already somewhere else
                if (
                    cand_to_discard.candidate_name != cand_to_keep.candidate_name and
                    cand_to_discard.candidate_name != cand_to_keep.person.name and
                    not cand_to_keep.person.other_names.filter(
                        name=cand_to_discard.candidate_name
                    ).exists()
                ):
                    keep.other_names.create(
                        name=cand_to_discard.candidate_name,
                        note='From merge of %s candidacies' % cand_to_keep.contest
                    )
                    cand_to_keep.refresh_from_db()

                # keep the candidacy sources
                if cand_to_discard.sources.exists():
                    for source in cand_to_discard.sources.all():
                        if not cand_to_keep.sources.filter(url=source.url).exists():
                            cand_to_keep.sources.create(
                                url=source.url,
                                note=source.note,
                            )
                        cand_to_keep.refresh_from_db()

                # keep earliest filed_date
                if cand_to_keep.filed_date and cand_to_discard.filed_date:
                    if cand_to_keep.filed_date > cand_to_discard.filed_date:
                        cand_to_keep.filed_date = cand_to_discard.filed_date
                elif cand_to_discard.filed_date:
                    cand_to_keep.filed_date = cand_to_discard.filed_date
                # keep is_incumbent if True
                if not cand_to_keep.is_incumbent and cand_to_discard.is_incumbent:
                    cand_to_keep.is_incumbent = cand_to_discard.is_incumbent
                # assuming not trying to merge candidacies with different parties
                if not cand_to_keep.party and cand_to_discard.party:
                    cand_to_keep.party = cand_to_discard.party

                cand_to_keep.save()
                cand_to_discard.delete()

        keep.refresh_from_db()

        # make sure Person name is same as most recent candidate_name
        latest_candidate_name = keep.candidacies.latest(
            'contest__election__date',
        ).candidate_name
        if keep.name != latest_candidate_name:
            # move current Person.name into other_names
            if not keep.other_names.filter(name=keep.name).exists():
                keep.other_names.create(name=keep.name)
            keep.name = latest_candidate_name
        keep.save()

        return keep


class OCDPersonProxy(Person, OCDProxyModelMixin):
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

        # If we've made it this far, it's time to add
        name, created = self.other_names.get_or_create(name=name, note=note)
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

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDPersonNameProxy(PersonName, OCDProxyModelMixin):
    """
    A proxy on the OCD PersonName model with helper methods.
    """

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
