#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals

# Models
from opencivicdata.core.models import (
    Membership,
    Organization,
    OrganizationIdentifier,
    OrganizationName,
)
from .people import OCDPersonProxy
from ..base import OCDProxyModelMixin

# Managers
from postgres_copy import CopyQuerySet
from calaccess_processed.managers import (
    OCDOrganizationManager,
    OCDMembershipManager
)

# Logging
import logging
logger = logging.getLogger(__name__)


class OCDOrganizationProxy(Organization, OCDProxyModelMixin):
    """
    A proxy on the OCD Organization model with helper methods.
    """
    objects = OCDOrganizationManager.from_queryset(CopyQuerySet)()

    copy_to_fields = (
        ('id',),
        ('name',),
        ('image',),
        ('parent_id',),
        ('jurisdiction_id',),
        ('classification',),
        ('founding_date',),
        ('dissolution_date',),
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


class OCDOrganizationIdentifierProxy(OrganizationIdentifier, OCDProxyModelMixin):
    """
    A proxy on the OCD OrganizationIdentifier model with helper methods.
    """
    objects = CopyQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDOrganizationNameProxy(OrganizationName, OCDProxyModelMixin):
    """
    A proxy on the OCD OrganizationName model with helper methods.
    """
    objects = CopyQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDMembershipProxy(Membership, OCDProxyModelMixin):
    """
    A proxy on the OCD Membership model with helper methods.
    """
    objects = OCDMembershipManager.from_queryset(CopyQuerySet)()

    copy_to_fields = (
        ('id',),
        ('organization_id',),
        ('person_id',),
        ('person_name',),
        ('post_id',),
        ('on_behalf_of_id',),
        ('label',),
        ('role',),
        ('start_date',),
        ('end_date',),
        ('created_at',),
        ('updated_at',),
        ('extras',),
        ('locked_fields',),
    )

    @property
    def person_proxy(self):
        """
        Returns an OCDPersonProxy instance linked to the Membership.
        """
        person = self.person
        person.__class__ = OCDPersonProxy
        return person

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
