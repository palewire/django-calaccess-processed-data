#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy model for augmenting ScrapedPropositionElection model with methods useful for processing.
"""
from __future__ import unicode_literals
import re
from django.utils import timezone
from calaccess_scraped.models import PropositionElection
from .base import ElectionProxyMixin


class ScrapedPropositionElectionProxy(ElectionProxyMixin, PropositionElection):
    """
    A proxy for the PropositionElection model in calaccess_scraped.
    """
    NAME_PATTERN = re.compile(r'^(?P<date>^[A-Z]+\s\d{1,2},\s\d{4}),?\s(?P<type>.+)$')

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True

    @property
    def election_type(self):
        """
        Return the scraped incumbent election's type.

        (e.g., "GENERAL", "PRIMARY", "SPECIAL ELECTION", "RECALL")
        """
        # Extract the name and date from the election name
        match = self.NAME_PATTERN.match(self.name)

        return match.groupdict()['type'].upper()

    @property
    def date(self):
        """
        Parse date from scraped proposition election's name.

        Return a timezone aware date object, if found, else None.
        """
        # Extract the name and date from the election name
        match = self.NAME_PATTERN.match(self.name)

        # Convert it to a datetime object
        return timezone.datetime.strptime(match.groupdict()['date'], '%B %d, %Y').date()

    def get_ocd_election(self):
        """
        Returns an OCD Election object for this record, if it exists.
        """
        from ..opencivicdata.elections import OCDElectionProxy
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
