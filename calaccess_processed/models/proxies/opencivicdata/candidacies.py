#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from calaccess_processed.models.json_funcs import (
    JSONArrayLength,
    JSONExtractPath,
    MaxFromJSONIntegerArray,
)
from django.db import models
from django.db.models import (
    IntegerField,
    Case,
    Count,
    F,
    Max,
    Q,
    When,
)
from django.db.models.functions import Cast
from opencivicdata.core.models import Membership
from opencivicdata.elections.models import (
    Candidacy,
    CandidateContest,
    CandidacySource,
)
from postgres_copy import CopyQuerySet
from .base import OCDProxyModelMixin
from .elections import OCDElectionProxy
from .people import OCDPersonProxy


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
            Q(candidate_name=name) |
            Q(person__name=name) |
            Q(person__other_names__name=name)
        ).distinct()

        if not q.exists():
            raise OCDCandidacyProxy.DoesNotExist(
                'OCDCandidacyProxy matching query does not exist'
            )
        elif q.count() > 1:
            raise OCDCandidacyProxy.MultipleObjectsReturned(
                'get_by_name() returned more than one OCDCandidacyProxy -- it returned %s!' % q.count()
            )
        else:
            return q[0]


class OCDCandidacyManager(models.Manager):
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


class OCDCandidacyProxy(Candidacy, OCDProxyModelMixin):
    """
    A proxy on the OCD Candidacy model with helper methods.
    """
    objects = OCDCandidacyManager.from_queryset(CopyQuerySet)()

    copy_to_fields = (
        ('id',),
        ('candidate_name',),
        ('person',),
        ('party',),
        ('contest',),
        ('post',),
        ('is_incumbent',),
        ('registration_status',),
        ('top_ticket_candidacy',),
        ('filed_date',),
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

    @property
    def election_proxy(self):
        """
        Returns the proxied OCDElectionProxy linked to this candidacy.
        """
        return OCDElectionProxy.objects.get(id=self.contest.election_id)

    @property
    def filer_ids(self):
        """
        Returns the CAL-ACCESS filer_id linked with the object, if any.
        """
        return self.person.identifiers.filter(scheme="calaccess_filer_id")

    @property
    def form501_filing_ids(self):
        """
        Returns any linked Form 501 filing ids.
        """
        try:
            return self.extras['form501_filing_ids']
        except KeyError:
            return []

    @property
    def form501s(self):
        """
        Returns any linked Form 501 objects.
        """
        from calaccess_processed.models import Form501Filing
        return Form501Filing.objects.filter(filing_id__in=self.form501_filing_ids)

    @property
    def person_proxy(self):
        """
        Returns an OCDPersonProxy instance linked to the Candidacy.
        """
        person = self.person
        person.__class__ = OCDPersonProxy
        return person

    def link_form501(self, form501_id):
        """
        Link an id of a Form501Filing to a Candidacy, if it isn't already.
        """
        # Check if the attribute is already there
        if 'form501_filing_ids' in self.extras:
            # If it is, check if we already have this id
            if form501_id not in self.extras['form501_filing_ids']:
                # If we don't, append it to the list
                self.extras['form501_filing_ids'].append(form501_id)
                # Save out
                self.save()
        # If the attribute isn't there, go ahead and add it.
        else:
            self.extras['form501_filing_ids'] = [form501_id]
            # Save out
            self.save()

    def update_from_form501(self):
        """
        Set Candidacy fields using data extracted from linked Form501Filings.
        """
        from calaccess_processed.models import Form501Filing

        # get all Form501Filing linked to Candidacy
        filing_ids = self.extras['form501_filing_ids']
        filings = Form501Filing.objects.filter(filing_id__in=filing_ids)

        # keep the earliest filed_date
        first_filed_date = filings.earliest('date_filed').date_filed

        # Update filed_date if not the earliest
        if self.filed_date != first_filed_date:
            self.filed_date = first_filed_date
            self.save()

        # set registration status to "withdrawn" based on statement_type of latest Form501
        latest = filings.latest('date_filed')
        if latest.statement_type == '10003':  # <-- This is the code for withdrawn
            # If the candidacy hasn't been marked that way, update it now
            if self.registration_status != 'withdrawn':
                self.registration_status = 'withdrawn'
                self.save()

    def link_filer_ids_from_form501s(self):
        """
        Create PersonIdentifiers for each filer_id from Form501Filings.
        """
        from calaccess_processed.models import Form501Filing
        person = self.person
        current_filer_ids = [
            i.identifier for i in person.identifiers.filter(scheme='calaccess_filer_id')
        ]

        filing_ids = self.extras['form501_filing_ids']
        missing_filer_ids = [
            f.filer_id for f in Form501Filing.objects.filter(
                filing_id__in=filing_ids
            ).exclude(
                filer_id__in=current_filer_ids
            )
        ]
        for i in missing_filer_ids:
            person.identifiers.get_or_create(
                scheme='calaccess_filer_id',
                identifier=i,
            )

    def update_party_from_form501(self):
        """
        Update party for Candidacy based on latest Form501 where its populated.
        """
        from calaccess_processed.models import Form501Filing

        # get all Form501Filing linked to Candidacy
        filing_ids = self.extras['form501_filing_ids']
        filings = Form501Filing.objects.filter(filing_id__in=filing_ids)

        latest_party = filings.filter(
            party__isnull=False
        ).latest('date_filed').get_party()

        if latest_party != self.party:
            self.party = latest_party
            self.save()

    def check_incumbency(self):
        """
        Check if the Candidacy is for the incumbent officeholder.

        Return True if:
        * Membership exists for the Person and Post linked to the Candidacy, and
        * Membership.end_date is NULL or has a year later than Election.date.year.
        """
        incumbent_q = Membership.objects.filter(
            post=self.post,
            person=self.person,
        ).annotate(
            # Cast end_date's value as an int, treat '' as NULL
            end_year=Cast(
                Case(When(end_date='', then=None)),
                IntegerField(),
            )
        ).filter(
            Q(end_year__gt=self.election.date.year) |
            Q(end_date='')
        )
        if incumbent_q.exists():
            return True
        else:
            return False


class OCDCandidacySourceProxy(CandidacySource, OCDProxyModelMixin):
    """
    A proxy on the OCD CandidacySource model.
    """
    objects = CopyQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDFlatCandidacyManager(models.Manager):
    """
    Custom manager for flattening the contents of the OCD Candidacy model.
    """
    def get_queryset(self):
        """
        Returns the custom QuerySet for this manager.
        """
        return super(
            OCDFlatCandidacyManager, self
        ).get_queryset().filter(
            Q(person__identifiers__scheme='calaccess_filer_id') |
            Q(person__identifiers__isnull=True)
        ).annotate(
            name=F('candidate_name'),
            office=F('post__label'),
            party_name=F('party__name'),
            election_name=F('contest__election__name'),
            election_date=F('contest__election__date'),
            special_election=F('contest__previous_term_unexpired'),
            ocd_person_id=F('person__id'),
            ocd_candidacy_id=F('id'),
            ocd_election_id=F('contest__election'),
            ocd_post_id=F('post__id'),
            ocd_contest_id=F('contest'),
            ocd_party_id=F('party'),
            latest_calaccess_filer_id=Max('person__identifiers__identifier'),
            calaccess_filer_id_count=Count('person__identifiers__identifier'),
            latest_form501_filing_id=MaxFromJSONIntegerArray(
                'extras', 'form501_filing_ids'
            ),
            form501_filing_count=JSONArrayLength(
                JSONExtractPath('extras', 'form501_filing_ids')
            ),
        )


class OCDFlatCandidacyProxy(Candidacy, OCDProxyModelMixin):
    """
    Every candidate for a public office.
    """
    objects = OCDFlatCandidacyManager.from_queryset(CopyQuerySet)()

    copy_to_fields = (
        ('name',),
        ('party_name',
         'Name of the political party that nominated the candidate or would '
         'nominate the candidate (as in the case of a partisan primary).',),
        ('election_name',),
        ('election_date',),
        ('office',
         'Public office for which the candidate is seeking election.',),
        ('is_incumbent',),
        ('special_election', CandidateContest._meta.get_field('previous_term_unexpired').help_text),
        ('created_at',),
        ('updated_at',),
        ('ocd_person_id', Candidacy._meta.get_field('person').help_text),
        ('ocd_candidacy_id',),
        ('ocd_election_id', CandidateContest._meta.get_field('election').help_text),
        ('ocd_post_id', Candidacy._meta.get_field('post').help_text),
        ('ocd_contest_id', Candidacy._meta.get_field('contest').help_text),
        ('ocd_party_id', Candidacy._meta.get_field('party').help_text),
        ('latest_calaccess_filer_id',
         'Most recent filer_id assigned to the person in CAL-ACCESS.',),
        ('calaccess_filer_id_count',
         'Count of filer_ids assigned to the person in CAL-ACCESS.',),
        ('latest_form501_filing_id', "CAL-ACCESS identifier for the candidate's "
                                     "most recent Form 501 filing."),
        ('form501_filing_count', 'Count of Form 501s filed by the candidate.'),
    )

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
        verbose_name_plural = 'candidates'
