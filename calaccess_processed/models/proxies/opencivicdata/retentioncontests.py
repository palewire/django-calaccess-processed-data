#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db import models
from django.db.models import F, Max, Q
from opencivicdata.elections.models import (
    RetentionContest,
    RetentionContestIdentifier,
    RetentionContestOption,
    RetentionContestSource,
)
from .base import OCDProxyModelMixin
from postgres_copy import CopyQuerySet


class OCDRetentionContestProxy(RetentionContest, OCDProxyModelMixin):
    """
    A proxy on the OCD RetentionContest model.
    """
    objects = CopyQuerySet.as_manager()

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


class OCDFlatRetentionContestManager(models.Manager):
    """
    Custom manager for flattening contents of the OCD RetentionContest model.
    """
    def get_queryset(self):
        """
        Returns the custom QuerySet for this manager.
        """
        return super(
            OCDFlatRetentionContestManager, self
        ).get_queryset().filter(
            Q(identifiers__scheme='calaccess_measure_id') |
            Q(identifiers__isnull=True)
        ).annotate(
            office=F('membership__post__label'),
            person_name=F('membership__person__name'),
            ocd_person_id=F('membership__person__id'),
            election_name=F('election__name'),
            election_date=F('election__date'),
            ocd_contest_id=F('id'),
            ocd_post_id=F('membership__post_id'),
            ocd_membership_id=F('membership_id'),
            ocd_election_id=F('election_id'),
            calaccess_measure_id=Max('identifiers__identifier')
        )


class OCDFlatRetentionContestProxy(RetentionContest, OCDProxyModelMixin):
    """
    A proxy model for flattening the contents of the OCD RetentionContest model.
    """
    objects = OCDFlatRetentionContestManager.from_queryset(CopyQuerySet)()

    copy_to_fields = (
        'name',
        'person_name',
        'office',
        'election_name',
        'election_date',
        'description',
        'ocd_contest_id',
        'ocd_person_id',
        'ocd_post_id',
        'ocd_membership_id',
        'ocd_election_id',
        'created_at',
        'updated_at',
        'calaccess_measure_id',
    )

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
