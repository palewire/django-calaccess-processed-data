#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom fields.
"""
from django.core.exceptions import FieldDoesNotExist


class CopyToField(object):
    """
    Class to hold meta data about a field included in a CopyTo query.
    """
    def __init__(self, query, name, **kwargs):
        """
        Create a new instance of CopyToField.
        """
        self.query = query
        self.name = name
        self._help_text = kwargs.get('help_text', None)

    @property
    def choices(self):
        """
        Choices of the field.
        """
        return self.field.choices

    @property
    def description(self):
        """
        Description of the field.
        """
        return self.field.description % self.field.__dict__

    @property
    def field(self):
        """
        Django model Field instance.
        """
        return self.resolved_ref.field

    @property
    def help_text(self):
        """
        Help text of the field.
        """
        if self._help_text:
            help_text = self._help_text
        else:
            # return the help_text of the field as defined on the base model, if there
            try:
                help_text = self.query.model._meta.get_field(self.name).help_text
            except FieldDoesNotExist:
                help_text = self.field.help_text

        return help_text

    @property
    def resolved_ref(self):
        """
        Col expression resolved from reference.
        """
        return self.query.resolve_ref(self.name)
