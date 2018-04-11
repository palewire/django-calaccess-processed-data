#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom manager for the OCD Organization model.
"""
from __future__ import unicode_literals
from calaccess_raw.models import FilerToFilerTypeCd
from calaccess_processed.managers import BulkLoadSQLManager


class OCDPartyManager(BulkLoadSQLManager):
    """
    Limited the OCD Organization model to politics parties.
    """
    def get_queryset(self):
        """
        Override the default manager to limit the results to political parties.
        """
        return super(OCDPartyManager, self).get_queryset().filter(classification='party')

    def unknown(self):
        """
        Returns the UNKNOWN party.
        """
        return self.get_queryset().get(name='UNKNOWN')

    def get_by_name(self, name):
        """
        Helper for getting the OCD party object giving a raw name from CAL-ACCESS.

        If not found, return the "UNKNOWN" Organization object.
        """
        # First try a full name
        try:
            return self.get_queryset().get(name=name)
        except self.model.DoesNotExist:
            pass

        # If that doesn't work, try an alternate name
        try:
            return self.get_queryset().get(other_names__name=name)
        except self.model.DoesNotExist:
            pass

        # And if that doesn't work, just return the unknown party object
        return self.unknown()

    def get_by_filer_id(self, filer_id, election_date):
        """
        Lookup the party for the given filer_id, effective before election_date.

        If not found, return the "UNKNOWN" Organization object.
        """
        # Try to see if the record exists in the raw data with a party code
        try:
            party_code = FilerToFilerTypeCd.objects.filter(
                filer_id=filer_id,
                effect_dt__lte=election_date,
            ).latest('effect_dt').party_cd
        except FilerToFilerTypeCd.DoesNotExist:
            # If it doesn't hit just quit now
            return self.unknown()

        # IF we have a code, transform "INDEPENDENT" and "NON-PARTISAN" codes to "NO PARTY PREFERENCE"
        if party_code in [16007, 16009, 0]:
            party_code = 16012

        # Try pulling out the party using the lookup code
        try:
            return self.get_queryset().get(identifiers__identifier=party_code)
        except self.model.DoesNotExist:
            pass

        # If that fails, just quit and return the unknown party object
        return self.unknown()
