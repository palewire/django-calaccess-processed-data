#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals

# Models
from ..base import OCDProxyModelMixin
from opencivicdata.core.models import Post

# Managers
from postgres_copy import CopyQuerySet
from calaccess_processed.managers import (
    OCDPostManager,
    OCDAssemblyPostManager,
    OCDExecutivePostManager,
    OCDSenatePostManager
)


class OCDPostProxy(Post, OCDProxyModelMixin):
    """
    A proxy on the OCD Post model with helper methods..
    """
    objects = OCDPostManager.from_queryset(CopyQuerySet)()
    assembly = OCDAssemblyPostManager()
    executive = OCDExecutivePostManager()
    senate = OCDSenatePostManager()

    copy_to_fields = (
        ('id',),
        ('label',),
        ('role',),
        ('organization_id',),
        ('division_id',),
        ('start_date',),
        ('end_date',),
        ('maximum_memberships',),
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
