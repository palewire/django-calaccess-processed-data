#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
import re
from datetime import date
from django.utils import timezone
from ..opencivicdata.elections import OCDElectionProxy
from calaccess_scraped.models import PropositionElection


class ScrapedPropositionElectionProxy(PropositionElection):
    """
    A proxy for the PropositionElection model in calaccess_scraped.
    """
    NAME_PATTERN = re.compile(r'^(?P<date>^[A-Z]+\s\d{1,2},\s\d{4})\s(?P<name>.+)$')

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True

    def is_primary(self):
        """
        Returns whether or now the election was a primary.
        """
        return 'PRIMARY' in self.parsed_name.upper()

    def is_general(self):
        """
        Returns whether or now the election was a general election.
        """
        return 'GENERAL' in self.parsed_name.upper()

    def is_special(self):
        """
        Returns whether or now the election was a special election.
        """
        return 'SPECIAL' in self.parsed_name.upper()

    def is_recall(self):
        """
        Returns whether or now the election was a recall.
        """
        return 'RECALL' in self.parsed_name.upper()

    @property
    def parsed_name(self):
        """
        Parse a scraped candidate election name into its constituent parts.

        Parts include:
        * Four-digit year (int)
        * Type (str), e.g., "GENERAL", "PRIMARY", "SPECIAL ELECTION", "SPECIAL RUNOFF")
        * Office (optional str)
        * District (optional int)

        Returns a dict with year, type, office and district as keys.
        """
        # Extract the name and date from the election name
        match = self.NAME_PATTERN.match(self.name)

        # Convert it to a datetime object
        date_obj = timezone.datetime.strptime(match.groupdict()['date'], '%B %d, %Y').date()

        # Format that as a string
        name = '{0} {1}'.format(date_obj.year, match.groupdict()['name']).upper()

        # Differentiate between two '2008 PRIMARY' ballot measure elections
        if name == '2008 PRIMARY' and date_obj.month == 2:
            name = "2008 PRESIDENTIAL PRIMARY AND SPECIAL ELECTIONS"

        return name

    @property
    def parsed_date(self):
        """
        Use a scraped candidate election name to look up the election date.

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
        # If this is the 2008 recall or primary we have a hacked out edge case solution
        if self.name == 'JUNE 3, 2008 RECALL':
            return OCDElectionProxy.objects.get(name__icontains="RECALL", date=date(2008, 6, 3))
        elif self.name == 'JUNE 3, 2008 PRIMARY':
            return OCDElectionProxy.objects.get(name__icontains="PRIMARY", date=date(2008, 6, 3))

        # Otherwise proceed by trying to get the record via its date
        return OCDElectionProxy.objects.get(date=self.parsed_date)
