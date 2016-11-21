#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Helper utilities for the model's in this application.
"""
from django.db import models
from collections import OrderedDict
from django.template.defaultfilters import title


class BaseModel(models.Model):
    """
    A base class for all models.
    """
    class Meta:
        """
        Model options.
        """
        abstract = True

    def meta(self):
        """
        Return's the model's _meta options.
        """
        return self._meta

    def klass(self):
        """
        Return the model's class constructor.
        """
        return self.__class__

    def doc(self):
        """
        Returns the model's docstring.
        """
        return self.__doc__

    def to_dict(self):
        """
        Returns the model object as a vanilla Python dictionary.
        """
        d = OrderedDict({})
        for f in self._meta.fields:
            d[f.verbose_name] = getattr(self, f.name)
        return d


class AllCapsNameMixin(BaseModel):
    """
    Abstract model with name cleaners we can reuse across models.
    """
    class Meta:
        """
        Model options.
        """
        abstract = True

    def __unicode__(self):
        return self.clean_name

    @property
    def short_name(self, character_limit=60):
        """
        A trimmed version of the clean name.
        """
        if len(self.clean_name) > character_limit:
            return self.clean_name[:character_limit] + "..."
        return self.clean_name

    @property
    def clean_name(self):
        """
        A cleaned up version of ALL CAPS names provided by the source data.
        """
        n = self.name
        n = n.strip()
        n = n.lower()
        n = title(n)
        n = n.replace("A. D.", "A.D.")
        force_lowercase = ['Of', 'For', 'To', 'By']
        for fl in force_lowercase:
            s = []
            for p in n.split(" "):
                if p in force_lowercase:
                    s.append(p.lower())
                else:
                    s.append(p)
            n = " ".join(s)
        force_uppercase = [
            'Usaf', 'Pac', 'Ca', 'Ad', 'Rcc', 'Cdp', 'Aclu',
            'Cbpa-Pac', 'Aka', 'Aflac',
        ]
        for fl in force_uppercase:
            s = []
            for p in n.split(" "):
                if p in force_uppercase:
                    s.append(p.upper())
                else:
                    s.append(p)
            n = " ".join(s)
        n = n.replace("Re-Elect", "Re-elect")
        n = n.replace("Political Action Committee", "PAC")
        return n
