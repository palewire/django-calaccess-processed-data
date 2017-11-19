#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load OCD Filing and related models from Form460Filing and related models.
"""

from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models import (
    OCDCommitteeProxy,
    OCDCommitteeIdentifierProxy,
    OCDCommitteeTypeProxy,
    OCDCommitteeNameProxy,
    OCDFilingProxy,
    OCDFilingIdentifierProxy,
    OCDFilingActionProxy,
    OCDFilingActionSummaryAmountProxy,
    OCDTransactionProxy,
)


class Command(CalAccessCommand):
    """
    Load OCD Filing and related models from Form460Filing and related models.
    """
    help = 'Load and archive the CAL-ACCESS Filing and FilingVersion models.'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        self.header('Loading data extracted from Form 460 filings')

        if not OCDCommitteeTypeProxy.objects.exists():
            OCDCommitteeTypeProxy.objects.seed()

        OCDCommitteeProxy.objects.load_form460_data()
        self.duration()
        OCDCommitteeIdentifierProxy.objects.load_form460_data()
        self.duration()
        OCDCommitteeNameProxy.objects.load_form460_data()
        self.duration()

        OCDFilingProxy.objects.load_form460_data()
        self.duration()
        OCDFilingIdentifierProxy.objects.load_form460_data()
        self.duration()

        OCDFilingActionProxy.objects.load_form460_data()
        self.duration()
        OCDFilingActionSummaryAmountProxy.objects.load_form460_data()
        self.duration()

        OCDTransactionProxy.objects.load_form460_data()
        self.duration()

        self.success("Done!")
