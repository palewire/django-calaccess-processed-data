#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base classes for OCD models and model fields.
"""
from __future__ import unicode_literals
import re
import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.validators import RegexValidator
from calaccess_processed.models.opencivicdata import common


class OCDIDField(models.CharField):
    """
    Custom model field for implementing unique ID in OCD's format.
    """
    def __init__(self, *args, **kwargs):
        """
        Custom __init__ method of OCDIDField.
        """
        self.ocd_type = kwargs.pop('ocd_type')
        if self.ocd_type != 'jurisdiction':
            kwargs['default'] = lambda: 'ocd-{}/{}'.format(self.ocd_type, uuid.uuid4())
            # len('ocd-') + len(ocd_type) + len('/') + len(uuid)
            #       = 4 + len(ocd_type) + 1 + 36
            #       = len(ocd_type) + 41
            kwargs['max_length'] = 41 + len(self.ocd_type)
            regex = '^ocd-' + self.ocd_type + '/[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$'
        else:
            kwargs['max_length'] = 300
            regex = common.JURISDICTION_ID_REGEX

        kwargs['primary_key'] = True
        # get pattern property if it exists, otherwise just return the object (hopefully a string)
        msg = 'ID must match ' + getattr(regex, 'pattern', regex)
        kwargs['validators'] = [RegexValidator(regex=regex, message=msg, flags=re.U)]
        super(OCDIDField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        """
        Custom deconstruct method for OCDIDField.
        """
        name, path, args, kwargs = super(OCDIDField, self).deconstruct()
        if self.ocd_type != 'jurisdiction':
            kwargs.pop('default')
        kwargs.pop('max_length')
        kwargs.pop('primary_key')
        kwargs['ocd_type'] = self.ocd_type
        return (name, path, args, kwargs)


class OCDBase(models.Model):
    """
    Abstract base model with common fields for all OCD models.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Time that this object was created at in the system.',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Time that this object was last updated in the system.',
    )
    extras = JSONField(
        default=dict,
        blank=True,
        help_text='Common to all Open Civic Data types, the value is a '
                  'key-value store suitable for storing arbitrary information '
                  'not covered elsewhere.',
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


class RelatedBase(models.Model):
    """
    Abstract base class for related models.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        """
        Model options.
        """
        abstract = True


class LinkBase(RelatedBase):
    """
    Abstract base class for related link models.
    """
    note = models.CharField(max_length=300, blank=True)
    url = models.URLField(max_length=2000)

    class Meta:
        """
        Model options.
        """
        abstract = True

    def __str__(self):
        return self.url


class MimetypeLinkBase(RelatedBase):
    """
    Abstract base class for related mime type link models.
    """
    media_type = models.CharField(max_length=100)
    url = models.URLField(max_length=2000)
    text = models.TextField(default='', blank=True)

    class Meta:
        """
        Model options.
        """
        abstract = True


class IdentifierBase(RelatedBase):
    """
    Abstract base class for related identifier models.
    """
    identifier = models.CharField(max_length=300)
    scheme = models.CharField(max_length=300)

    class Meta:
        """
        Model options.
        """
        abstract = True

    def __str__(self):
        return self.identifier


class RelatedEntityBase(RelatedBase):
    """
    Abstract base class for related entity models.
    """
    name = models.CharField(max_length=2000)
    entity_type = models.CharField(max_length=20, blank=True)

    # optionally tied to an organization or person if it was linkable
    organization = models.ForeignKey('Organization', null=True)
    person = models.ForeignKey('Person', null=True)

    @property
    def entity_name(self):
        """
        Returns the name of the related entity, whether it is a person or org.
        """
        if self.entity_type == 'organization' and self.organization_id:
            return self.organization.name
        elif self.entity_type == 'person' and self.person_id:
            return self.person.name
        else:
            return self.name

    @property
    def entity_id(self):
        """
        Returns the id of the related entity, whether it is a person or org.
        """
        if self.entity_type == 'organization':
            return self.organization_id
        if self.entity_type == 'person':
            return self.person_id
        return None

    class Meta:
        """
        Model options.
        """
        abstract = True
