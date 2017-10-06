#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check for mistakes in processed data loaded from CAL-ACCESS.
"""
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models import OCDElectionProxy
from django.utils import timezone


class Command(CalAccessCommand):
    """
    Check for mistakes in processed data loaded from CAL-ACCESS.
    """
    help = 'Check for mistakes in processed data loaded from CAL-ACCESS.'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        self.check_elections()

    def check_elections(self):
        """
        Check counts of contests in elections.
        """
        elections = OCDElectionProxy.objects.filter(
            date__year__lte=timezone.now().year
        )
        for election in elections:
            self.log(' Checking %s' % election)
            election.verify_regular_exec_contest_count()
            self.log('  Executive offices verified.')
            election.verify_regular_senate_contest_count()
            election.verify_regular_senate_contest_districts()
            self.log('  State Senate offices verified.')
            election.verify_regular_assembly_contest_count()
            self.log('  State Assembly offices verified.')
