#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from opencivicdata.elections.models import (
    BallotMeasureContest,
    BallotMeasureContestIdentifier,
    BallotMeasureContestOption,
    BallotMeasureContestSource,
)
from ..base import OCDProxyModelMixin
from postgres_copy import CopyQuerySet


class OCDBallotMeasureContestProxy(BallotMeasureContest, OCDProxyModelMixin):
    """
    A proxy on the OCD BallotMeasureContest model.
    """
    objects = CopyQuerySet.as_manager()

    copy_to_fields = (
        ('id',),
        ('name',),
        ('division_id',),
        ('election_id',),
        ('description',),
        ('requirement',),
        ('classification',),
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


class OCDBallotMeasureContestIdentifierProxy(BallotMeasureContestIdentifier, OCDProxyModelMixin):
    """
    A proxy on the OCD BallotMeasureContestIdentifier model.
    """
    objects = CopyQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDBallotMeasureContestOptionProxy(BallotMeasureContestOption, OCDProxyModelMixin):
    """
    A proxy on the OCD BallotMeasureContestOption model.
    """
    objects = CopyQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDBallotMeasureContestSourceProxy(BallotMeasureContestSource, OCDProxyModelMixin):
    """
    A proxy on the OCD BallotMeasureContestSource model.
    """
    objects = CopyQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
