#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.apps import apps
from calaccess_processed.managers import BulkLoadSQLManager


class RawFilerToFilerTypeCdManager(BulkLoadSQLManager):
    """
    Custom helpers for the calaccess_raw FilerToFilerTypeCd model.
    """
    def get_office_by_filer_id_and_date(self, filer_id, election_date):
        """
        Lookup the office for the given filer_id, effective before election_date.

        Return a string containg the office name and district number (if applicable),
        or None if not found.
        """
        LookupCodesCd = apps.get_model("calaccess_raw", "LookupCodesCd")

        # Try a straight query for it
        try:
            ftft = self.get_queryset().filter(filer_id=filer_id, effect_dt__lte=election_date).latest('effect_dt')
        except (self.model.DoesNotExist, ValueError):
            # If you don't find it, quit.
            return None

        # Look up the race type
        try:
            office = LookupCodesCd.objects.get(code_id=ftft.race)
        except (LookupCodesCd.DoesNotExist, LookupCodesCd.MultipleObjectsReturned):
            # If you can't find it, quit.
            return None

        # If we don't have a valid district code, just return the name.
        if not ftft.district_cd or ftft.district_cd == 0:
            return "{}".format(office).strip()

        # Otherwise, get the district and tack that on
        try:
            district = LookupCodesCd.objects.get(code_id=ftft.district_cd)
        except (LookupCodesCd.DoesNotExist, LookupCodesCd.MultipleObjectsReturned):
            return None

        # If you found a district, return the string with office combined in there
        return '{} {}'.format(office, district).strip()
