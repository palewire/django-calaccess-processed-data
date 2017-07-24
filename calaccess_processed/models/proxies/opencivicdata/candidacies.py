#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db import models
from django.db.models import IntegerField
from django.db.models import Case, When, Q
from django.db.models.functions import Cast
from opencivicdata.core.models import Membership
from opencivicdata.elections.models import Candidacy


class OCDCandidacyManager(models.Manager):
    """
    Manager for custom methods on the OCDCandidacyProxy model.
    """
    def matched_form501_ids(self):
        """
        Return all the Form 501 filing ids matched to a candidacy record.
        """
        return [
            i['extras']['form501_filing_ids'] for i in
            self.get_queryset().filter(extras__has_key='form501_filing_ids').values('extras')
        ]

    def get_by_filer_id(self, filer_id):
        """
        Returns a Candidacy object linked to a CAL-ACCESS filer_id, if it exists.
        """
        return self.get_queryset().get(
            person__identifiers__scheme='calaccess_filer_id',
            person__identifiers__identifier=filer_id,
        )


class OCDCandidacyProxy(Candidacy):
    """
    A proxy on the OCD Candidacy model with helper methods.
    """
    objects = OCDCandidacyManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True

    def link_form501(self, form501):
        """
        Link a Form501Filing to a Candidacy, if it isn't already.
        """
        # Check if the attribute is already there
        if 'form501_filing_ids' in self.extras:
            # If it is, check if we already have this id
            if form501.filing_id not in self.extras['form501_filing_ids']:
                # If we don't, append it to the list
                self.extras['form501_filing_ids'].append(form501.filing_id)
                # Save out
                self.save()
        # If the attribute isn't there, go ahead and add it.
        else:
            self.extras['form501_filing_ids'] = [form501.filing_id]
            # Save out
            self.save()

    def update_from_form501(self, form501):
        """
        Set Candidacy fields using data extracted from linked Form501Filings.
        """
        from calaccess_processed.models import Form501Filing

        # get all Form501Filing linked to Candidacy
        filing_ids = self.extras['form501_filing_ids']
        filings = Form501Filing.objects.filter(filing_id__in=filing_ids)

        # keep the earliest filed_date
        first_filed_date = filings.earliest('date_filed').date_filed

        # If the filed dates don't match, update them
        if self.filed_date != first_filed_date:
            self.filed_date = first_filed_date
            self.save()

        # keep going if latest filing says withdrawn
        latest = filings.latest('date_filed')
        if latest.statement_type == '10003':  # <-- This is the code for withdrawn
            # If the candidacy hasn't been marked that way, update it now
            if self.registration_status != 'withdrawn':
                self.registration_status = 'withdrawn'
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
