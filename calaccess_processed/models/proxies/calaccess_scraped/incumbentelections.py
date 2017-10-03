#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy model for augmenting ScrapedIncumbentElection model with methods useful for processing.
"""
from __future__ import unicode_literals
from calaccess_scraped.models import IncumbentElection
from django.db.models import Manager
from postgres_copy import CopyQuerySet
from .base import ElectionProxyMixin
from ..opencivicdata.elections import OCDElectionProxy


class ScrapedIncumbentElectionManager(Manager):
    """
    Manager with custom queryset and methods on the ScrapedIncumbentElectionProxy model.
    """
    def get_queryset(self):
        """
        Override the default manager to exclude blacklisted elections.
        """
        # http://www.sos.ca.gov/elections/prior-elections/special-elections/
        blacklisted_elections = (
            '2017-10-2',
            '2015-11-30',
            '2015-9-28',
            '2014-9-29',
            '2014-3-17',
            '2001-3-6',
        )
        return super(
            ScrapedIncumbentElectionManager, self
        ).get_queryset().exclude(date__in=blacklisted_elections)


class ScrapedIncumbentElectionProxy(ElectionProxyMixin, IncumbentElection):
    """
    A proxy for the IncumbentElection model in calaccess_scraped.
    """
    objects = ScrapedIncumbentElectionManager.from_queryset(CopyQuerySet)()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True

    def get_ocd_election(self):
        """
        Returns an OCD Election object for this record, if it exists.
        """
        try:
            ocd_election = OCDElectionProxy.objects.get(
                name=self.ocd_name,
                date=self.date,
            )
        except OCDElectionProxy.DoesNotExist:
            # If that doesn't exist, try getting it by date
            try:
                ocd_election = OCDElectionProxy.objects.get(date=self.date)
            except (
                OCDElectionProxy.DoesNotExist,
                OCDElectionProxy.MultipleObjectsReturned
            ):
                raise

        return ocd_election

    @property
    def election_type(self):
        """
        Return the scraped incumbent election's type.

        (e.g., "GENERAL", "PRIMARY", "SPECIAL ELECTION", "SPECIAL RUNOFF")
        """
        if self.name == 'SPECIAL ELECTION':
            election_type = self.name
        else:
            election_type = self.name.replace('ELECTION', '').strip()

        return election_type
