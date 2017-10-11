#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check for mistakes in processed data loaded from CAL-ACCESS.
"""
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.tests.test_commands import ProcessedDataTest


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

        processed_data_tests = ProcessedDataTest()

        try:
            processed_data_tests.test_regular_executive_contest_counts()
        except AssertionError as err:
            self.failure(err)
        else:
            self.log('  State Executive office contests verified.')

        try:
            processed_data_tests.test_regular_senate_contest_counts()
        except AssertionError as err:
            self.failure(err)
        else:
            self.log('  State Senate contests verified.')

        try:
            processed_data_tests.test_regular_senate_contest_districts()
        except AssertionError as err:
            self.failure(err)
        else:
            self.log('  State Senate districts verified.')

        try:
            processed_data_tests.test_regular_assembly_contest_counts()
        except AssertionError as err:
            self.failure(err)
        else:
            self.log('  State Assembly contests verified.')

        try:
            processed_data_tests.test_for_duplicate_memberships()
        except AssertionError as err:
            self.failure(err)
        else:
            self.log('  Memberships verified.')
