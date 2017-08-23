#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db.models import F
from opencivicdata.elections.models import (
    BallotMeasureContest,
    BallotMeasureContestIdentifier,
    BallotMeasureContestOption,
    BallotMeasureContestSource,
)
from .base import OCDProxyModelMixin


class OCDBallotMeasureContestProxy(BallotMeasureContest, OCDProxyModelMixin):
    """
    A proxy on the OCD BallotMeasureContest model.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDBallotMeasureContestIdentifierProxy(BallotMeasureContestIdentifier, OCDProxyModelMixin):
    """
    A proxy on the OCD BallotMeasureContestIdentifier model.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDBallotMeasureContestOptionProxy(BallotMeasureContestOption, OCDProxyModelMixin):
    """
    A proxy on the OCD BallotMeasureContestOption model.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDBallotMeasureContestSourceProxy(BallotMeasureContestSource, OCDProxyModelMixin):
    """
    A proxy on the OCD BallotMeasureContestSource model.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDFlatBallotMeasureContestProxy(BallotMeasureContest, OCDProxyModelMixin):
    """
    A proxy on the OCD BallotMeasureContest model for exporting a flattened csv of ballot measures.
    """
    copy_to_expressions = dict(
        measure=F('name'),
        type=F('classification'),
        election_name=F('election__name'),
        election_date=F('election__date'),
        ocd_id=F('id'),
        desc=F('description'),
        created=F('created_at'),
        updated=F('updated_at'),
    )

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
