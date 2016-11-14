#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for campaign entity models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.Candidate)
class CandidateAdmin(BaseAdmin):
    """
    Custom admin for the Candidate model.
    """
    list_display = (
        'filer_id',
        'last_name',
        'first_name',
        'middle_name',
        'name_suffix',
        'election_year',
        'f501_filing_id',
        'last_f501_amend_id',
        'office',
        'district',
        'agency',
        'party',
    )


@admin.register(models.CandidateCommittee)
class CandidateCommitteeAdmin(BaseAdmin):
    """
    Custom admin for the CandidateCommittee model.
    """
    list_display = (
        'candidate_filer_id',
        'committee_filer_id',
        'link_type_id',
        'link_type_description',
        'first_session',
        'last_session',
        'first_effective_date',
        'last_effective_date',
        'first_termination_date',
        'last_termination_date',
    )
