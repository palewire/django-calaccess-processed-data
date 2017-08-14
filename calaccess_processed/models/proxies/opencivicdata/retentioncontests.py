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
