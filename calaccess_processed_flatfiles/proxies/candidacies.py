#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for generating flatfiles that combine multiple table into a simplified file.
"""
from __future__ import unicode_literals
from calaccess_processed.proxies import OCDProxyModelMixin
from opencivicdata.elections.models import Candidacy, CandidateContest
from calaccess_processed_flatfiles.managers import OCDFlatCandidacyManager


class OCDFlatCandidacyProxy(Candidacy, OCDProxyModelMixin):
    """
    Every candidate for a public office.
    """
    objects = OCDFlatCandidacyManager()

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
        app_label = "calaccess_processed_flatfiles"
        proxy = True
        verbose_name_plural = 'candidates'
