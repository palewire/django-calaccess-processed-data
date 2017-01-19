#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OCD Person and Organization-related models and manager.

Copied (with some modifications) from
https://github.com/opencivicdata/python-opencivicdata-django/blob/master/opencivicdata/models/people_orgs.py
"""
import datetime
from django.db import models
from django.db.models import Q, QuerySet
from .base import OCDBase, LinkBase, OCDIDField, RelatedBase, IdentifierBase
from .division import Division
from .jurisdiction import Jurisdiction
from .common import CONTACT_TYPE_CHOICES, ORGANIZATION_CLASSIFICATION_CHOICES

# abstract models


class ContactDetailBase(RelatedBase):
    """
    Abstract base class for OCD ContactDetail models.
    """
    type = models.CharField(max_length=50, choices=common.CONTACT_TYPE_CHOICES)
    value = models.CharField(max_length=300)
    note = models.CharField(max_length=300, blank=True)
    label = models.CharField(max_length=300, blank=True)

    class Meta:
        """
        Model options.
        """
        abstract = True

    def __str__(self):
        return '{}: {}'.format(self.get_type_display(), self.value)


class OtherNameBase(RelatedBase):
    """
    Abstract base class for OCD OtherName models.
    """
    name = models.CharField(max_length=500, db_index=True)
    note = models.CharField(max_length=500, blank=True)
    start_date = models.CharField(max_length=10, blank=True)    # YYYY[-MM[-DD]]
    end_date = models.CharField(max_length=10, blank=True)      # YYYY[-MM[-DD]]

    class Meta:
        """
        Model options.
        """
        abstract = True

    def __str__(self):
        return '{} ({})'.format(self.name, self.note)


# the actual models
class Organization(OCDBase):
    """
    OCD Organization model, as defined in OCDEP 5: People, Organizations, Posts, and Memberships.
    """
    id = OCDIDField(ocd_type='organization')
    name = models.CharField(max_length=300)
    image = models.URLField(blank=True, max_length=2000)
    parent = models.ForeignKey('self', related_name='children', null=True)
    jurisdiction = models.ForeignKey(Jurisdiction, related_name='organizations', null=True)
    classification = models.CharField(max_length=100, blank=True,
                                      choices=common.ORGANIZATION_CLASSIFICATION_CHOICES)
    founding_date = models.CharField(max_length=10, blank=True)     # YYYY[-MM[-DD]]
    dissolution_date = models.CharField(max_length=10, blank=True)  # YYYY[-MM[-DD]]

    def __str__(self):
        return self.name

    # Access all "ancestor" organizations
    def get_parents(self):
        """
        Returns the org's parent orgs.
        """
        org = self
        while True:
            org = org.parent
            # Django accesses parents lazily, so have to check if one actually exists
            if org:
                yield org
            else:
                break

    def get_current_members(self):
        """
        Return all Person objects w/ current memberships to org.
        """
        today = datetime.date.today().isoformat()

        return Person.objects.filter(Q(memberships__start_date='') |
                                     Q(memberships__start_date__lte=today),
                                     Q(memberships__end_date='') |
                                     Q(memberships__end_date__gte=today),
                                     memberships__organization_id=self.id
                                     )

    class Meta:
        """
        Model options.
        """
        index_together = [
            ['jurisdiction', 'classification', 'name'],
            ['classification', 'name'],
        ]


class OrganizationIdentifier(IdentifierBase):
    """
    Model for storing an OCD Organization's other identifiers.
    """
    organization = models.ForeignKey(
        Organization,
        related_name='identifiers'
    )

    def __str__(self):
        tmpl = '%s identifies %s'
        return tmpl % (self.identifier, self.organization)


class OrganizationName(OtherNameBase):
    """
    Model for storing an OCD Organization's other names.
    """
    organization = models.ForeignKey(
        Organization,
        related_name='other_names'
    )


class OrganizationContactDetail(ContactDetailBase):
    """
    Model for storing an OCD Organization's contact details.
    """
    organization = models.ForeignKey(
        Organization,
        related_name='contact_details',
    )


class OrganizationLink(LinkBase):
    """
    Model for storing an OCD Organization's related links.
    """
    organization = models.ForeignKey(
        Organization,
        related_name='links'
    )


class OrganizationSource(LinkBase):
    """
    Model for storing an OCD Organization's related source links.
    """
    organization = models.ForeignKey(
        Organization,
        related_name='sources'
    )


class Post(OCDBase):
    """
    OCD Post model, as defined in OCDEP 5: People, Organizations, Posts, and Memberships.
    """
    id = OCDIDField(ocd_type='post')
    label = models.CharField(max_length=300)
    role = models.CharField(max_length=300, blank=True)
    organization = models.ForeignKey(Organization, related_name='posts')
    division = models.ForeignKey(
        Division,
        related_name='posts',
        null=True,
        blank=True,
        default=None
    )
    start_date = models.DateField(
        null=True,
    )
    end_date = models.DateField(
        null=True,
    )

    class Meta:
        """
        Model options.
        """
        index_together = [
            ['organization', 'label']
        ]

    def __str__(self):
        return '{} - {} - {}'.format(
            self.role,
            self.label,
            self.organization
        )


class PostContactDetail(ContactDetailBase):
    """
    Model for storing the ContactDetails of an OCD Post.
    """
    post = models.ForeignKey(Post, related_name='contact_details')


class PostLink(LinkBase):
    """
    Model for storing the related links of an OCD Post.
    """
    post = models.ForeignKey(Post, related_name='links')


class PersonQuerySet(QuerySet):
    """
    Custom queryset manager for OCD Person model.
    """
    def member_of(self, organization_name, current_only=True):
        """
        Returns the a queryset for accessing the Orgs or which the person is a member.
        """
        filter_params = []

        if current_only:
            today = datetime.date.today().isoformat()

            filter_params = [Q(memberships__start_date='') |
                             Q(memberships__start_date__lte=today),
                             Q(memberships__end_date='') |
                             Q(memberships__end_date__gte=today),
                             ]
        if organization_name.startswith('ocd-organization/'):
            qs = self.filter(
                *filter_params,
                memberships__organization_id=organization_name
            )
        else:
            qs = self.filter(
                *filter_params,
                memberships__organization__name=organization_name
            )
        return qs


class Person(OCDBase):
    """
    OCD Person model, as defined in OCDEP 5: People, Organizations, Posts, and Memberships.
    """
    objects = PersonQuerySet.as_manager()

    id = OCDIDField(ocd_type='person')
    name = models.CharField(max_length=300, db_index=True)
    sort_name = models.CharField(max_length=100, default='', blank=True)
    family_name = models.CharField(max_length=100, blank=True)
    given_name = models.CharField(max_length=100, blank=True)

    image = models.URLField(blank=True, max_length=2000)
    gender = models.CharField(max_length=100, blank=True)
    summary = models.CharField(max_length=500, blank=True)
    national_identity = models.CharField(max_length=300, blank=True)
    biography = models.TextField(blank=True)
    birth_date = models.DateField(
        null=True,
    )
    death_date = models.DateField(
        null=True,
    )

    def __str__(self):
        return self.name

    def add_other_name(self, name, note=""):
        """
        Custom method for adding an other name to an OCD Person.
        """
        PersonName.objects.create(
            name=name,
            note=note,
            person_id=self.id,
        )

    class Meta:
        """
        Model options.
        """
        verbose_name_plural = "people"


class PersonIdentifier(IdentifierBase):
    """
    Model for storing an OCD Person's other identifiers.
    """
    person = models.ForeignKey(Person, related_name='identifiers')


class PersonName(OtherNameBase):
    """
    Model for storing an OCD Person's other names.
    """
    person = models.ForeignKey(Person, related_name='other_names')


class PersonContactDetail(ContactDetailBase):
    """
    Model for storing an OCD Person's contact details.
    """
    person = models.ForeignKey(Person, related_name='contact_details')


class PersonLink(LinkBase):
    """
    Model for storing an OCD Person's related links.
    """
    person = models.ForeignKey(Person, related_name='links')


class PersonSource(LinkBase):
    """
    Model for storing an OCD Person's related links.
    """
    person = models.ForeignKey(Person, related_name='sources')


class Membership(OCDBase):
    """
    OCD Membership model, as defined in OCDEP 5: People, Organizations, Posts, and Memberships.
    """
    id = OCDIDField(ocd_type='membership')
    organization = models.ForeignKey(Organization, related_name='memberships')
    person = models.ForeignKey(Person, related_name='memberships')
    post = models.ForeignKey(Post, related_name='memberships', null=True)
    on_behalf_of = models.ForeignKey(Organization, related_name='memberships_on_behalf_of',
                                     null=True)
    label = models.CharField(max_length=300, blank=True)
    role = models.CharField(max_length=300, blank=True)
    start_date = models.CharField(max_length=10, blank=True)    # YYYY[-MM[-DD]]
    end_date = models.CharField(max_length=10, blank=True)      # YYYY[-MM[-DD]]

    class Meta:
        """
        Model options.
        """
        index_together = [
            ['organization', 'person', 'label', 'post']
        ]

    def __str__(self):
        return '{} in {} ({})'.format(self.person, self.organization, self.role)


class MembershipContactDetail(ContactDetailBase):
    """
    Model for storing contact details of an OCD Membership.
    """
    membership = models.ForeignKey(
        Membership,
        related_name='contact_details',
    )


class MembershipLink(LinkBase):
    """
    Model for storing related links of an OCD Membership.
    """
    membership = models.ForeignKey(Membership, related_name='links')
