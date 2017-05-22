#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load OCD Party model from LOOKUP_CODES_CD table in raw CAL-ACCESS data.
"""
import re
from calaccess_raw.models.common import LookupCodesCd
from calaccess_processed.management.commands import CalAccessCommand
from opencivicdata.models.elections import Party


class Command(CalAccessCommand):
    """
    Load OCD Party model from LOOKUP_CODES_CD table in raw CAL-ACCESS data.
    """
    help = 'Load OCD Party model from LOOKUP_CODES_CD table in raw CAL-ACCESS data'

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
        q = LookupCodesCd.objects.filter(code_type=16000).exclude(code_id=16000)

        for lc in q:
            party, created = Party.objects.get_or_create(
                name=lc.code_desc,
                # combine the first char of each word (except AND) in party name
                abbreviation=''.join(
                    re.findall(
                        r'([A-z])\w+',
                        lc.code_desc.upper().replace(' AND ', '')
                    )
                ),
                classification='party',
            )
            if created:
                if self.verbosity > 2:
                    self.log(" Created %s" % party)
                if party.name in ['DEMOCRATIC', 'REPUBLICAN']:
                    if party.name == 'DEMOCRATIC':
                        party.color = '1d0ee9'
                    if party.name == 'REPUBLICAN':
                        party.color = 'e91d0e'
                party.save()

            # keep the code_id too
            p_id, created = party.identifiers.get_or_create(
                scheme='calaccess_lookup_code_id',
                identifier=lc.code_id,
            )
            if created:
                if self.verbosity > 2:
                    self.log(
                        " {0.identifier} indentifies {0.organization.name}".format(p_id)
                    )

        return
