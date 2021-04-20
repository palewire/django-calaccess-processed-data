#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom managers for the OCD CandidateContest models.
"""
from __future__ import unicode_literals
from django.db.models import Q
from django.db import models
from postgres_copy import CopyQuerySet


class OCDCandidateContestQuerySet(CopyQuerySet):
    """
    Custom helpers for the OCD CandidateContest model that limit it to runoffs.
    """
    def set_parents(self):
        """
        Connect and save parent contests for all runoffs.
        """
        for obj in self.runoffs():
            # Carve out for the duplicate 2010 Assembly 43 runoffs until
            # I can figure out what I broke.
            obj.runoff_for_contest = obj.get_parent()
            obj.save()

    def assembly(self):
        """
        Filter to state assembly contests.
        """
        return self.filter(division__subtype2='sldl')

    def executive(self):
        """
        Filter to executive contests.
        """
        return self.filter(
            Q(posts__post__organization__name='California State Executive Branch')
            | Q(posts__post__organization__parent__name='California State Executive Branch')
        )

    def regular(self):
        """
        Filter to "regular" contests.
        """
        return self.filter(previous_term_unexpired=False)

    def runoffs(self):
        """
        Filter down to runoff CandidateContest instances.
        """
        return self.filter(name__contains='RUNOFF')

    def senate(self):
        """
        Filter to state senate contests.
        """
        return self.filter(division__subtype2='sldu')

    def special(self):
        """
        Filter to "special" contests.
        """
        return self.filter(previous_term_unexpired=True)


OCDCandidateContestManager = models.Manager.from_queryset(OCDCandidateContestQuerySet)
