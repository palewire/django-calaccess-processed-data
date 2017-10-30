#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base class for proxies to OCD models.
"""
import textwrap
from django.template.defaultfilters import capfirst
from django.core.exceptions import FieldDoesNotExist


class OCDProxyModelMixin(object):
    """
    Properties and methods shared by all OCD proxy models.
    """
    @property
    def base_model(self):
        """
        The model being proxied.
        """
        return self.__class__.__bases__[0]

    @property
    def meta(self):
        """
        The model's meta attributes.
        """
        return self._meta

    @property
    def is_flat(self):
        """
        True if the proxy model is used to flatten relational data models.
        """
        return 'Flat' in self._meta.object_name

    @property
    def file_name(self):
        """
        The name for the csv to which the model's contents will be dumped.

        If the model is a flat model proxy, return the model's verbose_name_plural
        in CamelCase. Otherwise, return the object_name of the base_model.
        """
        if self.is_flat:
            file_name = ''.join(
                x for x in str(self._meta.verbose_name_plural).title()
                if not x.isspace()
            )
        else:
            file_name = self.base_model._meta.object_name
        return file_name

    @property
    def display_name(self):
        """
        The version of the name for this model we prefer to display on public facing web pages.
        """
        if self.is_flat:
            return capfirst(self.meta.verbose_name_plural)
        else:
            return self.file_name

    @property
    def doc(self):
        """
        Doc string of the proxy model, or base_model (if not flat).
        """
        if self.is_flat:
            doc = textwrap.dedent(self.__doc__).strip()
        elif self.base_model.__doc__.startswith(self.base_model._meta.object_name):
            doc = ''
        else:
            doc = textwrap.dedent(self.base_model.__doc__).strip()
        return doc

    @property
    def klass_group(self):
        """
        The model's group.
        """
        if self.is_flat:
            group = "Flat"
        else:
            group = "Relational"
        return group

    def get_field_list(self):
        """
        Return all the fields on the model as a tuple.
        """
        try:
            self.copy_to_fields
        except AttributeError:
            fields = self._meta.fields
        else:
            q = self._meta.model.objects.all().query
            fields_list = []
            for f in self.copy_to_fields:
                if len(f) > 1:
                    field = CopyToField(q, f[0], help_text=f[1])
                else:
                    field = CopyToField(q, f[0])
                fields_list.append(field)
            fields = tuple(f for f in fields_list)

        return fields


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
