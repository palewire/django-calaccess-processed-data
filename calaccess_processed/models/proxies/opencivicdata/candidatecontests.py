#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db import models
from opencivicdata.elections.models import CandidateContest
from .base import OCDProxyModelMixin


class OCDCandidateContestManager(models.Manager):
    """
    Custom helpers for the OCD CandidateContest model that limit it to runoffs.
    """
    def runoffs(self):
        """
        Filter down to runoff CandidateContest instances.
        """
        return self.get_queryset().filter(name__contains='RUNOFF')

    def set_parents(self):
        """
        Connect and save parent contests for all runoffs.
        """
        for obj in self.runoffs():
            # Carve out for the duplicate 2010 Assembly 43 runoffs until
            # I can figure out what I broke.
            obj.runoff_for_contest = obj.get_parent()
            obj.save()


class OCDCandidateContestProxy(CandidateContest, OCDProxyModelMixin):
    """
    A proxy on the OCD CandidateContest model with helper methods.
    """
    objects = OCDCandidateContestManager()

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
