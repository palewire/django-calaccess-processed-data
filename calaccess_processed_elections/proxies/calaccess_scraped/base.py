#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Mixins for proxies of models from calaccess_scraped.
"""
from __future__ import unicode_literals
import re
from datetime import date


class ScrapedElectionProxyMixin(object):
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
        from ..opencivicdata.elections import OCDElectionProxy
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
        Returns whether or not this was a primary election held in the partisan era prior to 2012.
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


class ScrapedNameMixin(object):
    """
    Tools for cleaning up scraped candidate names.
    """
    @property
    def corrected_name(self):
        """
        Returns the scraped name with any corrections made.
        """
        fixes = {
            # http://www.sos.ca.gov/elections/prior-elections/statewide-election-results/primary-election-march-7-2000/certified-list-candidates/ # noqa
            'COURTRIGHT DONNA': 'COURTRIGHT, DONNA'
        }
        return fixes.get(self.name, self.name)

    @property
    def parsed_name(self):
        """
        Return a dict of formatted Person name field values.
        """
        # sort_name is undoctored name from scrape
        d = {
            'sort_name': self.name.strip()
        }

        # parse out these suffixes: JR, SR, II, III
        suffix_pattern = r'(?:^|\s)((?:[JS]R\.?)|(?:I{2,3}))(?:,|\s|$)'
        match = re.search(suffix_pattern, d['sort_name'])
        if match:
            # replace suffix with a comma
            # and replace any double commas, strip any trailing
            d['sort_name'] = d['sort_name'].replace(match.group(), ',').replace(',,', ',')
            d['sort_name'] = re.sub(r',\s?$', '', d['sort_name']).strip()

        # split once, strip and flip the sort_name to make name
        split_name = [i.strip() for i in d['sort_name'].split(',', 1)]
        name_list = list(split_name)
        name_list.reverse()
        d['name'] = ' '.join(name_list).strip()
        d['family_name'] = split_name[0]
        if len(split_name) > 1:
            d['given_name'] = split_name[1]
        if match:
            # append suffix to end of name and given_name
            suffix = ' %s' % match.group().replace(',', '').strip()
            d['name'] += suffix
            if 'given_name' in d:
                d['given_name'] += suffix

        return d

    def parse_office_name(self):
        """
        Parse string containg the name for an office.

        Expected format is "{TYPE NAME} [{DISTRICT NUMBER}]".

        Return a dict with two keys: type and district.
        """
        office_pattern = r'^(?P<type>[A-Z ]+)(?P<district>\d{2})?$'
        try:
            parsed = re.match(office_pattern, self.office_name.upper()).groupdict()
        except AttributeError:
            parsed = {'type': None, 'district': None}
        else:
            parsed['type'] = parsed['type'].strip()
            try:
                parsed['district'] = int(parsed['district'])
            except TypeError:
                pass
        return parsed
