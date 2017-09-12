#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base class for proxies to OCD models.
"""
import textwrap


class OCDProxyModelMixin(object):
    """
    Properties and methods shared by all OCD proxy models.
    """

    @property
    def base_model(self):
        """
        Returns the model class that is being proxied.
        """
        return self.__class__.__bases__[0]

    @property
    def is_flat(self):
        """
        Return True if the proxy model is used to flatten relational data models.
        """
        return 'Flat' in self._meta.object_name

    @property
    def object_name(self):
        """
        Return the model's object name as a string.

        If the model is flat model proxy, include the prefix "Flat". Otherwise,
        just use the object name of the model that is being proxied.
        """
        if self.is_flat:
            object_name = 'Flat%s' % self.model._meta.object_name
        else:
            object_name = self.model._meta.object_name
        return object_name

    @property
    def doc(self):
        """
        Returns doc string of the model corresponding to the ProcessedDataFile.
        """
        if self.model.__doc__.startswith(self.model._meta.object_name):
            return ''
        return textwrap.dedent(self.model.__doc__).strip()

    @property
    def klass_group(self):
        """
        Return the model's group.
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
        return self._help_text or self.field.help_text

    @property
    def resolved_ref(self):
        """
        Col expression resolved from reference.
        """
        return self.query.resolve_ref(self.name)
