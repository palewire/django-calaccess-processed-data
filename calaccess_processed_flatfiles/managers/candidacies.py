#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Managers for generating flatfiles that combine multiple table into a simplified file.
"""
from __future__ import unicode_literals
from calaccess_processed.postgres import (
    JSONArrayLength,
    JSONExtractPath,
    MaxFromJSONIntegerArray,
)
from django.db.models import F, Q
from django.db.models import Count, Max
from calaccess_processed.managers import BulkLoadSQLManager


class OCDFlatCandidacyManager(BulkLoadSQLManager):
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
            Q(person__identifiers__scheme='calaccess_filer_id')
            | Q(person__identifiers__isnull=True)
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
                'extras',
                'form501_filing_ids'
            ),
            form501_filing_count=JSONArrayLength(
                JSONExtractPath('extras', 'form501_filing_ids')
            ),
        )
