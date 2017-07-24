#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from opencivicdata.elections.models import Candidacy
from calaccess_processed.models import Form501FilingVersion


class OCDCandidacyProxy(Candidacy):
    """
    A proxy on the OCD Candidacy model with helper methods.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True

    def link_form501(self, form501):
        """
        Link a Form501Filing to a Candidacy, if it isn't already.
        """
        # Check if the attribute is already there
        if 'form501_filing_ids' in self.extras:
            # If it is, check if we already have this id
            if form501.id not in self.extras['form501_filing_ids']:
                # If we don't, append it to the list
                self.extras['form501_filing_ids'].append(form501.id)
                # Save out
                self.save()
        # If the attribute isn't there, go ahead and add it.
        else:
            self.extras['form501_filing_ids'] = [form501.id]
            # Save out
            self.save()

    def update_from_form501(self, form501):
        """
        Set Candidacy fields using data extracted from linked Form501Filings.
        """
        # get all Form501FilingVersions linked to Candidacy
        filing_ids = self.extras['form501_filing_ids']
        filings = Form501FilingVersion.objects.filter(filing_id__in=filing_ids)

        # keep the earliest filed_date
        first_filed_date = filings.earliest('date_filed').date_filed

        # If the filed dates don't match, update them
        if self.filed_date != first_filed_date:
            self.filed_date = first_filed_date
            self.save()

        # keep going if latest filing says withdrawn
        latest = filings.latest('date_filed')
        if latest.statement_type == '10003':  # <-- This is the code for withdrawn
            # If the candidacy hasn't been marked that way, update it now
            if self.registration_status != 'withdrawn':
                self.registration_status = 'withdrawn'
                self.save()
