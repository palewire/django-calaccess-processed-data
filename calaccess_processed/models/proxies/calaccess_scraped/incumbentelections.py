#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy model for augmenting ScrapedIncumbentElection model with methods useful for processing.
"""
from __future__ import unicode_literals

# Models
from .base import ElectionProxyMixin
from ..opencivicdata import OCDElectionProxy
from calaccess_scraped.models import IncumbentElection

# Managers
from postgres_copy import CopyQuerySet
from calaccess_processed.managers import ScrapedIncumbentElectionManager


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
