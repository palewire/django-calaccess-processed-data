#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db import models
from django.db.models import F, Max, Q
from opencivicdata.elections.models import (
    BallotMeasureContest,
    BallotMeasureContestIdentifier,
    BallotMeasureContestOption,
    BallotMeasureContestSource,
)
from .base import OCDProxyModelMixin
from calaccess_processed.managers import CopyToQuerySet


class OCDBallotMeasureContestProxy(BallotMeasureContest, OCDProxyModelMixin):
    """
    A proxy on the OCD BallotMeasureContest model.
    """
    objects = CopyToQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDBallotMeasureContestIdentifierProxy(BallotMeasureContestIdentifier, OCDProxyModelMixin):
    """
    A proxy on the OCD BallotMeasureContestIdentifier model.
    """
    objects = CopyToQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDBallotMeasureContestOptionProxy(BallotMeasureContestOption, OCDProxyModelMixin):
    """
    A proxy on the OCD BallotMeasureContestOption model.
    """
    objects = CopyToQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDBallotMeasureContestSourceProxy(BallotMeasureContestSource, OCDProxyModelMixin):
    """
    A proxy on the OCD BallotMeasureContestSource model.
    """
    objects = CopyToQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDFlatBallotMeasureContestManager(models.Manager):
    """
    Custom manager for flattening contents of the OCD BallotMeasureContest model.
    """
    def get_queryset(self):
        """
        Returns the custom QuerySet for this manager.
        """
        return super(
            OCDFlatBallotMeasureContestManager, self
        ).get_queryset().filter(
            Q(identifiers__scheme='calaccess_measure_id') |
            Q(identifiers__isnull=True)
        ).annotate(
            election_name=F('election__name'),
            election_date=F('election__date'),
            ocd_contest_id=F('id'),
            calaccess_measure_id=Max('identifiers__identifier')
        )


class OCDFlatBallotMeasureContestProxy(BallotMeasureContest, OCDProxyModelMixin):
    """
    A proxy model for flattening the contents of the OCD BallotMeasureContest model.
    """
    objects = OCDFlatBallotMeasureContestManager.from_queryset(CopyToQuerySet)()

    copy_to_fields = (
        'election_name',
        'election_date',
        'name',
        'classification',
        'description',
        'created_at',
        'updated_at',
        'ocd_contest_id',
        'calaccess_measure_id',
    )

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
