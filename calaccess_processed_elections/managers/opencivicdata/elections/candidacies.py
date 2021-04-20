#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db.models import Q
from postgres_copy import CopyQuerySet
from calaccess_processed.managers import BulkLoadSQLManager


class OCDCandidacyQuerySet(CopyQuerySet):
    """
    Custom QuerySet for the OCD Candidacy model.
    """
    def get_by_filer_id(self, filer_id):
        """
        Returns a Candidacy object linked to a CALACCESS filer_id, if it exists.
        """
        return self.get(
            person__identifiers__scheme='calaccess_filer_id',
            person__identifiers__identifier=filer_id,
        )

    def get_by_name(self, name):
        """
        Returns a Candidacy object with the provided name from the CALACCESS database or scrape.
        """
        q = self.filter(
            Q(candidate_name=name)
            | Q(person__name=name)
            | Q(person__other_names__name=name)
        ).distinct()

        if not q.exists():
            raise self.model.DoesNotExist('OCDCandidacyProxy matching query does not exist')
        elif q.count() > 1:
            raise self.model.MultipleObjectsReturned(
                'get_by_name() returned more than one OCDCandidacyProxy -- it returned %s!' % q.count()
            )
        else:
            return q[0]


class OCDCandidacyManager(BulkLoadSQLManager):
    """
    Manager for custom methods on the OCDCandidacyProxy model.
    """
    def get_queryset(self):
        """
        Returns the custom QuerySet for this manager.
        """
        return OCDCandidacyQuerySet(self.model, using=self._db)

    def matched_form501_ids(self):
        """
        Return all the Form 501 filing ids matched to a candidacy record.
        """
        return [
            i['extras']['form501_filing_ids'] for i in
            self.get_queryset().filter(extras__has_key='form501_filing_ids').values('extras')
        ]

    def get_or_create_from_calaccess(
        self,
        contest,
        candidate_name_dict,
        candidate_status="filed",
        candidate_filer_id=None
    ):
        """
        Get or create a Candidacy object with data from the CAL-ACCESS database.

        First, try getting an existing Candidacy within the given CandidateContest
        linked to a Person with the provided filer_id. If matched and the matched Person
        has different current name and doesn't have the provided name as an other name,
        add the other name.

        Next, try getting an existing Candidacy within the given CandidateContest
        linked to a Person with provided name (as default name or other name). If
        matched and match candidate doesn't already have filer_id, add the filer_id.

        If no match or if the matched person already has a different filer_id, create
        a new Candidacy (this may also create a new Person record).

        Returns a tuple (Candidacy object, created), where created is a boolean
        specifying whether a Candidacy was created.
        """
        from calaccess_processed_elections.proxies import OCDPersonProxy, OCDCandidacyProxy

        candidacy = None

        # first, try matching to existing candidate in contest with filer_id
        if candidate_filer_id:
            try:
                candidacy = self.model.objects.filter(contest=contest).get_by_filer_id(candidate_filer_id)
            except self.model.DoesNotExist:
                pass
            else:
                candidacy_created = False
                # if provided name not person's current name and not linked to person add it
                candidacy.person_proxy.add_other_name(
                    candidate_name_dict['name'],
                    'Matched on CandidateContest and calaccess_filer_id'
                )

        # if filer_id match fails (or no filer_id), try matching to candidate
        # in contest with provided name
        if not candidacy:
            try:
                candidacy = self.model.objects.filter(contest=contest).get_by_name(candidate_name_dict['name'])
            except self.model.DoesNotExist:
                pass
            else:
                candidacy_created = False
                # if filer_id provided
                if candidate_filer_id:
                    # check to make sure candidate with same name doesn't have diff filer_id
                    if candidacy.person.identifiers.filter(scheme='calaccess_filer_id').exists():
                        # if so, don't conflate
                        candidacy = None
                    else:
                        # if so, add filer_id to existing candidate
                        person = candidacy.person
                        person.refresh_from_db()
                        person.__class__ = OCDPersonProxy
                        person.add_filer_id(candidate_filer_id)

        # if no matched candidate yet, make a new one
        if not candidacy:
            # First make a Person object
            person, person_created = OCDPersonProxy.objects.get_or_create_from_calaccess(
                candidate_name_dict,
                candidate_filer_id=candidate_filer_id
            )
            person.add_other_name(candidate_name_dict['name'], 'From {} candidacy'.format(contest))

            # Then make the Candidacy
            candidacy = OCDCandidacyProxy.objects.create(
                contest=contest,
                person=person,
                post=contest.posts.all()[0].post,
                candidate_name=candidate_name_dict['name'],
                registration_status=candidate_status,
            )
            candidacy_created = True

        # if provided registration does not equal the default, update
        if candidate_status != 'filed' and candidate_status != candidacy.registration_status:
            candidacy.registration_status = candidate_status
            candidacy.save()

        # make sure Person name is same as most recent candidate_name
        person = candidacy.person
        person.refresh_from_db()
        person.__class__ = OCDPersonProxy
        person.update_name()

        # Pass it back out.
        return candidacy, candidacy_created
