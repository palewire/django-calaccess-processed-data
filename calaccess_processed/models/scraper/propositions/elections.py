#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing election information scraped from the CAL-ACCESS website.
"""
from __future__ import unicode_literals
import re
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.scraper.base import BaseScrapedElection


@python_2_unicode_compatible
class PropositionScrapedElection(BaseScrapedElection):
    """
    An election day scraped as part of the `scrapecalaccesspropositions` command.
    """
    def __str__(self):
        return self.name

    def get_or_create_election(self):
        """
        Get or create an OCD Election object using the PropositionScrapedElection name.

        Returns a tuple (Election object, created), where created is a boolean
        specifying whether a Election was created.
        """
        from calaccess_processed.models.opencivicdata.elections import Election

        prop_name_pattern = r'^(?P<date>^[A-Z]+\s\d{1,2},\s\d{4})\s(?P<name>.+)$'
        # extract the name and date
        match = re.match(prop_name_pattern, self.name)
        dt_obj = timezone.make_aware(
            timezone.datetime.strptime(
                match.groupdict()['date'],
                '%B %d, %Y',
            )
        )
        name = '{0} {1}'.format(
            dt_obj.year,
            match.groupdict()['name'],
        ).upper()
        # try getting an existing OCD election with the same date
        created = False
        try:
            elec = Election.objects.get(start_time=dt_obj)
        except Election.DoesNotExist:
            # or make a new one
            elec = Election.objects.create(start_time=dt_obj, name=name)
        else:
            created = True
            # if election already exists and is named 'SPECIAL' or 'RECALL'
            if (
                'SPECIAL' in elec.name.upper() or
                'RECALL' in elec.name.upper()
            ):
                # and the matched election's name includes either 'GENERAL'
                # or 'PRIMARY'...
                if (
                    re.match(r'^\d{4} GENERAL$', name) or
                    re.match(r'^\d{4} PRIMARY$', name)
                ):
                    # update the name
                    elec.name = name
                    elec.save()
        elec.sources.update_or_create(
            url=self.url,
            note='Last scraped on {dt:%Y-%m-%d}'.format(
                dt=self.last_modified,
            )
        )
        return (elec, created)
