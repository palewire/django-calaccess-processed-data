#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db.models import Q
from opencivicdata.elections.models import (
    CandidateContest,
    CandidateContestPost,
    CandidateContestSource,
)
from .base import OCDProxyModelMixin
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
            Q(posts__post__organization__name='California State Executive Branch') |
            Q(posts__post__organization__parent__name='California State Executive Branch')
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


class OCDCandidateContestProxy(CandidateContest, OCDProxyModelMixin):
    """
    A proxy on the OCD CandidateContest model with helper methods.
    """
    objects = OCDCandidateContestQuerySet.as_manager()

    copy_to_fields = (
        ('id',),
        ('name',),
        ('division_id',),
        ('election_id',),
        ('party_id',),
        ('previous_term_unexpired',),
        ('number_elected',),
        ('runoff_for_contest_id',),
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

    def get_parent(self):
        """
        Returns the undecided contest that preceeded runoff_contest.

        Returns None if it can't be found.
        """
        # Get the contest's post (should only ever be one per contest)
        post = self.posts.all()[0].post

        # Then try getting the most recent contest for the same post
        # that preceeds the runoff contest
        try:
            return CandidateContest.objects.filter(
                posts__post=post,
                election__date__lt=self.election.date,
            ).latest('election__date')
        except CandidateContest.DoesNotExist:
            return None


class OCDCandidateContestPostProxy(CandidateContestPost, OCDProxyModelMixin):
    """
    A proxy on the OCD CandidateContestPost model.
    """
    objects = CopyQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDCandidateContestSourceProxy(CandidateContestSource, OCDProxyModelMixin):
    """
    A proxy on the OCD CandidateContestSource model.
    """
    objects = CopyQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
