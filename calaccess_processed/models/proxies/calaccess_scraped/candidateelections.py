#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
import re
from datetime import date
from django.utils import timezone
from calaccess_processed import special_elections
from calaccess_scraped.models import CandidateElection, IncumbentElection
from .electionsbase import ElectionProxyMixin
from ..opencivicdata.elections import OCDElectionProxy


class ScrapedCandidateElectionProxy(ElectionProxyMixin, CandidateElection):
    """
    A proxy for the CandidateElection model in calaccess_scraped.
    """
    class Meta:
        """
        Make this a proxy model.
        """
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

    def guess_election_date(self, year, election_type):
        """
        Get the date of the election in the given year and type.

        Raise an exception if year is not even or if election_type is not "PRIMARY" or "GENERAL".

        Return a date object.
        """
        # Rules defined here:
        # https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=ELEC&division=1.&title=&part=&chapter=1.&article= # noqa

        # Parse out the data we need from the name
        parsed_year = self.parsed_name['year']

        # Make sure it's a regular election year
        if parsed_year % 2 != 0:
            raise Exception("Regular elections occur in even years.")
        elif self.is_primary:
            # Primary elections are in June
            month = 6
        elif self.is_general == 'GENERAL':
            # General elections are in November
            month = 11
        else:
            raise Exception("election_type must 'PRIMARY' or 'GENERAL'.")

        # get the first weekday
        # zero-indexed starting with monday
        first_weekday = date(parsed_year, month, 1).weekday()
        # calculate day or first tuesday after first monday
        day_or_month = (7 - first_weekday) % 7 + 2
        # Pass it out
        return date(year, month, day_or_month)

    @property
    def election_type(self):
        """
        Return the scraped incumbent election's type.

        (e.g., "GENERAL", "PRIMARY", "SPECIAL ELECTION", "SPECIAL RUNOFF")
        """
        return self.parsed_name['type']

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
            incumbent = IncumbentElection.objects.get(
                date__year=self.parsed_name['year'],
                name__icontains=self.parsed_name['type'],
            )
            return incumbent.date
        except (IncumbentElection.DoesNotExist, IncumbentElection.MultipleObjectsReturned):
            pass

        # If that doesn't work either, try parsing the election date from the name
        try:
            return self.guess_election_date()
        except:
            # If that fails, just give up and return None
            return None

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
        if parsed_name['office']:
            parsed_name['office'] = parsed_name['office'].strip()
        if parsed_name['district']:
            parsed_name['district'] = int(parsed_name['district'])

        # Pass it out
        return parsed_name


class ScrapedIncumbentElectionProxy(ElectionProxyMixin, IncumbentElection):
    """
    A proxy for the IncumbentElection model in calaccess_scraped.
    """
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
