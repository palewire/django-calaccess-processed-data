#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals

# Models
from calaccess_processed.proxies import OCDProxyModelMixin
from opencivicdata.core.models import Post

# Managers
from calaccess_processed_elections.managers import (
    OCDPostManager,
    OCDAssemblyPostManager,
    OCDExecutivePostManager,
    OCDSenatePostManager
)


class OCDPostProxy(Post, OCDProxyModelMixin):
    """
    A proxy on the OCD Post model with helper methods..
    """
    objects = OCDPostManager()
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
        app_label = "calaccess_processed_elections"
        proxy = True
