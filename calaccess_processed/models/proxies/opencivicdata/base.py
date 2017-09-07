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
    def is_flat(self):
        """
        Return True if the proxy model is used to flatten relational data models.
        """
        return 'Flat' in self._meta.object_name

    @property
    def model(self):
        """
        Returns the model class that is being proxied.
        """
        return self.__class__.__bases__[0]

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
        return "CCDC"

    def get_field_list(self):
        """
        Return all the fields on the model as a list.
        """
        if hasattr(self, 'copy_to_fields'):
            q = self._meta.model.objects.all().query
            fields = []
            for f in self.copy_to_fields:
                # get the Django models.field instance
                field = q.resolve_ref(f).field
                # set the name to alias used (if different)
                if field.name != f:
                    field.name = f
                fields.append(field)
        else:
            fields = self._meta.fields

        return fields
