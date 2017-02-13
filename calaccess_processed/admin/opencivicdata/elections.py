#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for OpenCivicData campaign models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.Election)
class ElectionAdmin(BaseAdmin):
    """
    Custom admin for the Election model.
    """
    list_display = (
        'name',
        'start_time',
        'administrative_org',
        'is_statewide'
    )
    search_fields = ('name',)
    date_hierarchy = 'start_time'


@admin.register(models.Party)
class PartyAdmin(BaseAdmin):
    """
    Custom admin for the Party model.
    """
    list_display = (
        'name',
        'abbreviation',
        'color',
    )
    search_fields = ('name',)


@admin.register(models.BallotMeasureContest)
class BallotMeasureContestAdmin(BaseAdmin):
    """
    Custom admin for the BallotMeasureContest model.
    """
    list_display = (
        "name",
        "election"
    )


@admin.register(models.BallotMeasureSelection)
class BallotMeasureSelectionAdmin(BaseAdmin):
    """
    Custom admin for the BallotMeasureSelection model.
    """
    list_display = (
        "contest_name",
        "selection"
    )


@admin.register(models.CandidateContest)
class CandidateContestAdmin(BaseAdmin):
    """
    Custom admin for the CandidateContest model.
    """
    list_display = (
        "name",
        "election"
    )


@admin.register(models.CandidateSelection)
class CandidateSelectionAdmin(BaseAdmin):
    """
    Custom admin for the CandidateSelection model.
    """
    list_display = (
        "contest_name",
    )


@admin.register(models.RetentionContest)
class RetentionContestAdmin(BaseAdmin):
    """
    Custom admin for the RetentionContest model.
    """
    list_display = (
        "name",
        "election"
    )


@admin.register(models.Candidacy)
class CandidacyAdmin(BaseAdmin):
    """
    Custom admin for the Candidacy model.
    """
    list_display = (
        "person",
        "post",
        "election"
    )
