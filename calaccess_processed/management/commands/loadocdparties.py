#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load OCD Organization model with parties extracted from raw CAL-ACCESS data.
"""
import re
from opencivicdata.core.models import Organization
from calaccess_raw.models.common import LookupCodesCd
from calaccess_processed.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Load OCD Organization model with parties extracted from raw CAL-ACCESS data.
    """
    help = 'Load OCD Organization model with parties extracted from raw CAL-ACCESS data'
    first_letters_regex = re.compile(r'([A-z])\w+')

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.header('Loading Parties')
        self.load()
        self.success("Done!")

    def load(self):
        """
        Insert Party records from the raw LOOKUP_CODES_CD table.
        """
        # Pull all of the raw LookupCodes in the 16000 code_type series
        # exclude the title entry of "PARTY CODE" with the identical number
        object_list = LookupCodesCd.objects.filter(code_type=16000).exclude(code_id=16000)

        # Loop through them all
        for obj in object_list:
            # Pull out the party name ...
            # ... but treat INDEPENDENT and NON-PARTISAN as NO PARTY PREFERENCE
            if obj.code_desc in ['INDEPENDENT', 'NON-PARTISAN', 'N/A', 'NON PARTISAN']:
                party_name = 'NO PARTY PREFERENCE'
            else:
                party_name = obj.code_desc

            # Get a party object from the OCD Organization model
            party, created = Organization.objects.get_or_create(name=party_name, classification='party')

            # If it's new...
            if created:
                # Log it out
                if self.verbosity > 2:
                    self.log(" Created %s party" % party)
                # Save abbreviation as an alternative party name
                # combine the first char of each word (except AND)
                trimmed_party = party_name.upper().replace(' AND ', '')
                first_letters = self.first_letters_regex.findall(trimmed_party)
                abbreviation = ''.join(first_letters)
                party.other_names.get_or_create(name=abbreviation, note='abbreviation')

            # keep the code_id too
            p_id, created = party.identifiers.get_or_create(
                scheme='calaccess_lookup_code_id',
                identifier=obj.code_id,
            )
