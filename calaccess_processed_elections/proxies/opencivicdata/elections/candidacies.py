#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db.models.functions import Cast

# Models
from django.db.models import (
    IntegerField,
    Case,
    Q,
    When
)
from .elections import OCDElectionProxy
from opencivicdata.core.models import Membership
from opencivicdata.elections.models import Candidacy, CandidacySource
from calaccess_processed.proxies import OCDProxyModelMixin
from ..core.people import OCDPersonProxy

# Managers
from calaccess_processed.managers import BulkLoadSQLManager
from calaccess_processed_elections.managers import OCDCandidacyManager


class OCDCandidacyProxy(Candidacy, OCDProxyModelMixin):
    """
    A proxy on the OCD Candidacy model with helper methods.
    """
    objects = OCDCandidacyManager()

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
        app_label = "calaccess_processed_elections"
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
        from calaccess_processed_filings.models import Form501Filing
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
        from calaccess_processed_filings.models import Form501Filing

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
        from calaccess_processed_filings.models import Form501Filing
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
        from calaccess_processed_filings.models import Form501Filing

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
            Q(end_year__gt=self.election.date.year)
            | Q(end_date='')
        )
        if incumbent_q.exists():
            return True
        else:
            return False


class OCDCandidacySourceProxy(CandidacySource, OCDProxyModelMixin):
    """
    A proxy on the OCD CandidacySource model.
    """
    objects = BulkLoadSQLManager()

    class Meta:
        """
        Make this a proxy model.
        """
        app_label = "calaccess_processed_elections"
        proxy = True
