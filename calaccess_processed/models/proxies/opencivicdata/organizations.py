#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db.models import Count, Manager
import logging
from opencivicdata.core.models import (
    Membership,
    Organization,
    OrganizationIdentifier,
    OrganizationName,
)
from .base import OCDProxyModelMixin
from .people import OCDPersonProxy
from postgres_copy import CopyQuerySet
logger = logging.getLogger(__name__)


class OCDOrganizationManager(Manager):
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


class OCDMembershipManager(Manager):
    """
    Manager for custom methods on the OCDMembershipProxy model.
    """
    def get_or_create_from_calaccess(self, incumbent):
        """
        Get or create and OCD Membership from a scraped incumbent.
        """
        from .people import OCDPersonProxy
        from .posts import OCDPostProxy
        # Get or create post
        post, post_created = OCDPostProxy.objects.get_or_create_by_name(
            incumbent.office_name,
        )
        if post_created:
            logger.debug(' Created new Post: %s' % post.label)
        # Get or create person
        person, person_created = OCDPersonProxy.objects.get_or_create_from_calaccess(
            incumbent.parsed_name,
            candidate_filer_id=incumbent.scraped_id,
        )
        if person_created:
            logger.debug(' Created new Person: %s' % person.name)
        # Get or create membership for post and person
        membership, membership_created = self.get_queryset().get_or_create(
            person=person,
            post=post,
            role=post.role,
            organization=post.organization,
        )

        incumbent_name = incumbent.parsed_name['name']

        if membership.person_name != incumbent_name:
            membership.person_name == incumbent_name
            membership.save()

        membership.person_proxy.add_other_name(
            incumbent_name, 'From scraped incumbent record'
        )

        return membership, membership_created

    def get_duplicates(self):
        """
        Return a QuerySet with duplicate Membership instances.
        """
        # group memberships by post_id and person_id
        # check if any group has more than one row.
        return self.get_queryset().values(
            'post', 'person'
        ).annotate(row_count=Count('id')).filter(row_count__gt=1)


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
