#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from datetime import date
from ..opencivicdata.elections import OCDElectionProxy


class ElectionProxyMixin(object):
    """
    Mixin with properties and methods shared by all scraped Election proxy models.
    """
    def get_or_create_ocd_election(self):
        """
        Get the OCD Election for the scraped election instance, or create a new one.

        Side effects of getting:
        * The scraped election's type will be appended to the 'calaccess_election_type'
        of the OCD Election's extras (if not already included).
        * The scraped election's scraped_id (if it exists) will be appended to the OCD
        Election's idenfitiers.

        Returns a tuple (Election object, created), where created is a boolean
        specifying whether a Election was created.
        """
        scraped_id = getattr(self, 'scraped_id', None)
        # Try getting the OCD election via the proxy's get method
        try:
            ocd_election = self.get_ocd_election()
        except OCDElectionProxy.DoesNotExist:
            # or create a new one
            ocd_election = OCDElectionProxy.objects.create_from_calaccess(
                self.ocd_name,
                self.date,
                election_id=scraped_id,
                election_type=self.election_type,
            )
            created = True
        else:
            created = False
            # If getting an existing election, add the election_type
            ocd_election.add_election_type(self.election_type)
            # and scraped_id
            if scraped_id:
                ocd_election.add_election_id(self.scraped_id)

            ocd_election.refresh_from_db()

        return ocd_election, created

    @property
    def is_primary(self):
        """
        Returns whether or now the election was a primary.
        """
        return 'PRIMARY' in self.name.upper()

    @property
    def is_general(self):
        """
        Returns whether or now the election was a general election.
        """
        return 'GENERAL' in self.name.upper()

    @property
    def is_special(self):
        """
        Returns whether or now the election was a special election.
        """
        return 'SPECIAL' in self.name.upper()

    @property
    def is_recall(self):
        """
        Returns whether or now the election was a recall.
        """
        return 'RECALL' in self.name.upper()

    @property
    def is_partisan_primary(self):
        """
        Returns whether or not this was a priamry election held in the partisan era prior to 2012.
        """
        if self.is_primary:
            if self.get_ocd_election().date.year < 2012:
                return True
        return False

    @property
    def ocd_name(self):
        """
        Return the name of the election in OCD format: {YEAR} {TYPE}.
        """
        # Add contests decided on 2/5/2008 should to an elecion named...
        if self.date == date(2008, 2, 5):
            ocd_name = "2008 PRESIDENTIAL PRIMARY AND SPECIAL ELECTIONS"
        # Add contests decided on 6/3/2008 should to an elecion named...
        elif self.date == date(2008, 6, 3):
            ocd_name = "2008 PRIMARY"
        # Otherwise return the format: "{YEAR} {ELECTION_TYPE}"
        else:
            ocd_name = '{0} {1}'.format(self.date.year, self.election_type)

        return ocd_name
