#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db import models
from opencivicdata.core.models import (
    Membership,
    Organization,
    OrganizationIdentifier,
    OrganizationName,
)
from .base import OCDProxyModelMixin
from postgres_copy import CopyQuerySet


class OCDOrganizationManager(models.Manager):
    """
    Custom helpers for the OCD Organization model.
    """
    def senate(self):
        """
        Returns state senate organization.
        """
        return self.get_queryset().get_or_create(
            name='California State Senate',
            classification='upper',
        )[0]

    def assembly(self):
        """
        Returns state assembly organization.
        """
        return self.get_queryset().get_or_create(
            name='California State Assembly',
            classification='lower',
        )[0]

    def executive_branch(self):
        """
        Returns executive branch organization.
        """
        return self.get_queryset().get_or_create(
            name='California State Executive Branch',
            classification='executive',
        )[0]

    def secretary_of_state(self):
        """
        Returns secretary of state organization.
        """
        return self.get_queryset().get_or_create(
            name='California Secretary of State',
            classification='executive',
            parent=self.executive_branch(),
        )[0]

    def elections_division(self):
        """
        Returns the elections division of the secretary of state organization.
        """
        return self.get_queryset().get_or_create(
            name='Elections Division',
            classification='executive',
            parent=self.secretary_of_state(),
        )[0]

    def board_of_equalization(self):
        """
        Returns board of equalization organization.
        """
        return self.get_queryset().get_or_create(
            name='State Board of Equalization',
            parent=self.executive_branch(),
        )[0]


class OCDOrganizationProxy(Organization, OCDProxyModelMixin):
    """
    A proxy on the OCD Organization model with helper methods.
    """
    objects = OCDOrganizationManager.from_queryset(CopyQuerySet)()

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
    objects = CopyQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
