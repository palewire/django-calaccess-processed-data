#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy model for augmenting ScrapedCandidateElection model with methods useful for processing.
"""
from __future__ import unicode_literals, absolute_import
import re
from datetime import date
from django.utils import timezone
from calaccess_processed_elections import get_expected_election_date, special_elections

# Models
from calaccess_scraped.models import CandidateElection
from .base import ScrapedElectionProxyMixin
from .incumbentelections import ScrapedIncumbentElectionProxy
from calaccess_processed_elections.proxies import OCDElectionProxy


class ScrapedCandidateElectionProxy(ScrapedElectionProxyMixin, CandidateElection):
    """
    A proxy for the CandidateElection model in calaccess_scraped.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        app_label = "calaccess_processed_elections"
        proxy = True

    def get_ocd_election(self):
        """
        Returns an OCD Election object for this record, if it exists.
        """
        # First, try getting the record via election's scraped_id
        try:
            return OCDElectionProxy.objects.get(
                identifiers__scheme='calaccess_election_id',
                identifiers__identifier=self.scraped_id,
            )
        except OCDElectionProxy.DoesNotExist:
            # If that doesn't exist, try getting it by date
            if self.date:
                return OCDElectionProxy.objects.get(date=self.date)
            else:
                # If that fails raise the DoesNotExist error
                raise

    @property
    def election_type(self):
        """
        Return the scraped incumbent election's type.

        (e.g., "GENERAL", "PRIMARY", "SPECIAL ELECTION", "SPECIAL RUNOFF")
        """
        return self.parsed_name['type']

    @property
    def is_recall(self):
        """
        This election is held to recall or retain one or more office holders.
        """
        return 'RECALL' in self.election_type

    @property
    def is_regular(self):
        """
        This is a regularly scheduled primary or general election.
        """
        return self.election_type == 'PRIMARY' or self.election_type == 'GENERAL'

    @property
    def is_special(self):
        """
        This is a special election or runoff outside of the regular election calendar.
        """
        return 'SPECIAL' in self.election_type

    @property
    def date(self):
        """
        Use a scraped candidate election name to look up the election date.

        Return a timezone aware date object, if found, else None.
        """
        # If this is the 2008, we have a hacked out edge case solution
        if self.name == '2008 PRIMARY':
            return date(2008, 6, 3)

        try:
            # Check if the date is in our hardcoded list of special election
            dt = special_elections.names_to_dates_dict[self.name]
            return timezone.datetime.strptime(dt, '%Y-%m-%d').date()
        except KeyError:
            pass

        # If not check the alternative list kept by the scraped IncumbentElection model
        try:
            incumbent_election = ScrapedIncumbentElectionProxy.objects.get(
                date__year=self.parsed_name['year'],
                name__icontains=self.parsed_name['type'],
            )
            return incumbent_election.date
        except (
            ScrapedIncumbentElectionProxy.DoesNotExist,
            ScrapedIncumbentElectionProxy.MultipleObjectsReturned,
        ):
            pass

        # If that doesn't work either, try parsing the election date from the name
        try:
            return get_expected_election_date(self.date.year, self.election_type)
        except ValueError:
            # If that fails, raise exception
            raise Exception(
                'Unknown date for %s. Check http://www.sos.ca.gov/elections/ '
                'and try adding missing date to '
                'calaccess_processed/special_elections.py' % self
            )

    @property
    def parsed_name(self):
        """
        Parse a scraped candidate election name into its constituent parts.

        Parts include:
        * Four-digit year (int)
        * Type (str), e.g., "GENERAL", "PRIMARY", "SPECIAL ELECTION", "SPECIAL RUNOFF"
        * Office (optional str)
        * District (optional int)

        Returns a dict with year, type, office and district as keys.
        """
        # Parse out the data
        pattern = r'^(?P<year>\d{4}) (?P<type>\b(?:[A-Z]| )+)(?: \((?P<office>(?:[A-Z]| )+)(?P<district>\d+)?\))?$' # NOQA
        parsed_name = re.match(pattern, self.name).groupdict()

        # Clean up the contents
        parsed_name['year'] = int(parsed_name['year'])
        parsed_name['type'] = parsed_name['type'].strip()

        # A special carveout for a 2018 election we know is a recall but the site has wrong.
        # http://www.sos.ca.gov/elections/upcoming-elections/2018-recall-sd29/
        if self.name == '2018 SPECIAL ELECTION (STATE SENATE 29)':
            parsed_name['type'] = "SPECIAL RECALL"

        if parsed_name['office']:
            parsed_name['office'] = parsed_name['office'].strip()
        if parsed_name['district']:
            parsed_name['district'] = int(parsed_name['district'])

        # Pass it out
        return parsed_name
