#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from opencivicdata.elections.models import (
    CandidateContest,
    CandidateContestPost,
    CandidateContestSource
)
from calaccess_processed.proxies import OCDProxyModelMixin
from calaccess_processed.managers import BulkLoadSQLManager
from calaccess_processed_elections.managers import OCDCandidateContestManager


class OCDCandidateContestProxy(CandidateContest, OCDProxyModelMixin):
    """
    A proxy on the OCD CandidateContest model with helper methods.
    """
    objects = OCDCandidateContestManager()

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
        app_label = "calaccess_processed_elections"
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
    objects = BulkLoadSQLManager()

    class Meta:
        """
        Make this a proxy model.
        """
        app_label = "calaccess_processed_elections"
        proxy = True


class OCDCandidateContestSourceProxy(CandidateContestSource, OCDProxyModelMixin):
    """
    A proxy on the OCD CandidateContestSource model.
    """
    objects = BulkLoadSQLManager()

    class Meta:
        """
        Make this a proxy model.
        """
        app_label = "calaccess_processed_elections"
        proxy = True
