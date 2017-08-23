#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db.models import F
from opencivicdata.elections.models import (
    RetentionContest,
    RetentionContestIdentifier,
    RetentionContestOption,
    RetentionContestSource,
)
from .base import OCDProxyModelMixin


class OCDRetentionContestProxy(RetentionContest, OCDProxyModelMixin):
    """
    A proxy on the OCD RetentionContest model.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDRetentionContestIdentifierProxy(RetentionContestIdentifier, OCDProxyModelMixin):
    """
    A proxy on the OCD RetentionContestIdentifier model.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDRetentionContestOptionProxy(RetentionContestOption, OCDProxyModelMixin):
    """
    A proxy on the OCD RetentionContestOption model.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDRetentionContestSourceProxy(RetentionContestSource, OCDProxyModelMixin):
    """
    A proxy on the OCD RetentionContestSource model.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDFlatRetentionContestProxy(RetentionContest, OCDProxyModelMixin):
    """
    A proxy on the OCD RetentionContest model for exporting a flattened csv of retention contest.
    """
    copy_to_expressions = dict(
        measure=F('name'),
        office=F('membership__post__label'),
        person_name=F('membership__person__name'),
        person_id=F('membership__person__id'),
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
