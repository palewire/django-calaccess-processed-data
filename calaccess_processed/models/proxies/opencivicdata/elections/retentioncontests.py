#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from opencivicdata.elections.models import (
    RetentionContest,
    RetentionContestIdentifier,
    RetentionContestOption,
    RetentionContestSource,
)
from ..base import OCDProxyModelMixin
from postgres_copy import CopyQuerySet


class OCDRetentionContestProxy(RetentionContest, OCDProxyModelMixin):
    """
    A proxy on the OCD RetentionContest model.
    """
    objects = CopyQuerySet.as_manager()

    copy_to_fields = (
        ('id',),
        ('name',),
        ('membership_id',),
        ('division_id',),
        ('election_id',),
        ('description',),
        ('requirement',),
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


class OCDRetentionContestIdentifierProxy(RetentionContestIdentifier, OCDProxyModelMixin):
    """
    A proxy on the OCD RetentionContestIdentifier model.
    """
    objects = CopyQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDRetentionContestOptionProxy(RetentionContestOption, OCDProxyModelMixin):
    """
    A proxy on the OCD RetentionContestOption model.
    """
    objects = CopyQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDRetentionContestSourceProxy(RetentionContestSource, OCDProxyModelMixin):
    """
    A proxy on the OCD RetentionContestSource model.
    """
    objects = CopyQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
