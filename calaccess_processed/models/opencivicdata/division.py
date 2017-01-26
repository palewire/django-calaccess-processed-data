#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OCD Division-related models and managers.

Copied (with some modifications) from
https://github.com/opencivicdata/python-opencivicdata-django/blob/master/opencivicdata/models/division.py
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.opencivicdata.base import OCDBase


class DivisionManager(models.Manager):
    """
    Manager with custom methods for OCD Division.
    """

    def children_of(self, division_id, subtype=None, depth=1):
        """
        Custom query method for getting the children of a division.
        """
        query, n = Division.subtypes_from_id(division_id)
        q_objects = []

        # only get children
        if subtype:
            query['subtype{0}'.format(n)] = subtype
        else:
            q_objects.append(~models.Q(**{'subtype{0}'.format(n): ''}))
        q_objects.append(~models.Q(**{'subid{0}'.format(n): ''}))

        # allow for depth wildcards
        n += depth

        # ensure final field is null
        q_objects.append(models.Q(**{'subtype{0}'.format(n): ''}))
        q_objects.append(models.Q(**{'subid{0}'.format(n): ''}))

        return self.filter(*q_objects, **query)

    def create(self, id, name, redirect=None):
        """
        Custom create method for Division objects.
        """
        return super(
            DivisionManager,
            self,
        ).create(
            id=id,
            name=name,
            redirect=redirect,
            **Division.subtypes_from_id(id)[0]
        )

    def load(self, state=None):
        """
        Custom method for loading OCD divisions from repo.
        """
        import requests

        url = 'https://raw.githubusercontent.com/opencivicdata/ocd-division-ids/master/identifiers/country-us.csv'  # NOQA
        r = requests.get(url, stream=True)

        lines = r.iter_lines(decode_unicode=True)
        # skip first line
        next(lines)
        for line in lines:
            cols = line.split(',')

            id_dict = {
                c.split(':')[0]: c.split(':')[1] for c in cols[0].split('/')[1:]
            }

            if state:
                if 'state' in id_dict and id_dict['state'] == state.lower():
                    self.create(id=cols[0], name=cols[1])
            else:
                self.create(id=cols[0], name=cols[1])

        return


@python_2_unicode_compatible
class Division(OCDBase):
    """
    Division as defined in OCDEP 2: Division Identifiers.

    A political geography such as a state, county, or congressional district,
    which may have multiple boundaries over its lifetime.
    """
    objects = DivisionManager()

    id = models.CharField(max_length=300, primary_key=True)
    name = models.CharField(max_length=300)
    redirect = models.ForeignKey('self', null=True)
    country = models.CharField(max_length=2)

    # up to 7 pieces of the id that are searchable
    subtype1 = models.CharField(max_length=50, blank=True)
    subid1 = models.CharField(max_length=100, blank=True)
    subtype2 = models.CharField(max_length=50, blank=True)
    subid2 = models.CharField(max_length=100, blank=True)
    subtype3 = models.CharField(max_length=50, blank=True)
    subid3 = models.CharField(max_length=100, blank=True)
    subtype4 = models.CharField(max_length=50, blank=True)
    subid4 = models.CharField(max_length=100, blank=True)
    subtype5 = models.CharField(max_length=50, blank=True)
    subid5 = models.CharField(max_length=100, blank=True)
    subtype6 = models.CharField(max_length=50, blank=True)
    subid6 = models.CharField(max_length=100, blank=True)
    subtype7 = models.CharField(max_length=50, blank=True)
    subid7 = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.id)
    __unicode__ = __str__

    @staticmethod
    def subtypes_from_id(division_id):
        """
        Extract the division's sub-types from its ID.
        """
        pieces = [piece.split(':', 1) for piece in division_id.split('/')]
        fields = {}

        # if it included the ocd-division bit, pop it off
        if pieces[0] == ['ocd-division']:
            pieces.pop(0)

        if pieces[0][0] != 'country':
            raise ValueError('OCD id must start with country')

        fields['country'] = pieces[0][1]

        # add the remaining pieces
        n = 1
        for stype, subid in pieces[1:]:
            fields['subtype{0}'.format(n)] = stype
            fields['subid{0}'.format(n)] = subid
            n += 1

        return fields, n
