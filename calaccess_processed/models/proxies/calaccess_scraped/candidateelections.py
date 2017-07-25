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
from opencivicdata.elections.models import Election
from calaccess_scraped.models import CandidateElection, IncumbentElection


class ScrapedCandidateElectionProxy(CandidateElection):
    """
    A proxy for the CandidateElection model in calaccess_scraped.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True

    def is_primary(self):
        """
        Returns whether or now the election was a primary.
        """
        return 'PRIMARY' in self.name.upper()

    def is_general(self):
        """
        Returns whether or now the election was a general election.
        """
        return 'GENERAL' in self.name.upper()

    def is_special(self):
        """
        Returns whether or now the election was a special election.
        """
        return 'SPECIAL' in self.name.upper()

    def is_recall(self):
        """
        Returns whether or now the election was a recall.
        """
        return 'RECALL' in self.name.upper()

    def is_partisan_primary(self):
        """
        Returns whether or not this was a priamry election held in the partisan era prior to 2012.
        """
        if self.is_primary():
            if self.get_ocd_election().date.year < 2012:
                return True
        return False

    def get_ocd_election(self):
        """
        Returns an OCD Election object for this record, if it exists.
        """
        # If this is the 2008, we have a hacked out edge case solution
        if self.name == '2008 PRIMARY':
            return Election.objects.get(name=self.name, date=date(2008, 6, 3))

        # Otherwise proceed by trying to get the record via its scraped id
        try:
            return Election.objects.get(
                identifiers__scheme='calaccess_election_id',
                identifiers__identifier=self.scraped_id,
            )
        except Election.DoesNotExist:
            # If that doesn't exist, try getting it by date
            if self.parsed_date:
                return Election.objects.get(date=self.parsed_date)
            else:
                # If that fails raise the DoesNotExist error
                raise

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

    @property
    def parsed_date(self):
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
        parsed_type = self.parsed_name['type']

        # Make sure it's a regular election year
        if parsed_year % 2 != 0:
            raise Exception("Regular elections occur in even years.")
        elif parsed_type.upper() == 'PRIMARY':
            # Primary elections are in June
            month = 6
        elif parsed_type.upper() == 'GENERAL':
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
