#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for management commands.
"""
from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from calaccess_processed.management.commands import CalAccessCommand


class ProcessedDataCommandsTest(TestCase):
    """
    Run and test management commands.
    """
    fixtures = [
        'divisions.json',
        'candidate_scraped_elections.json',
        'scraped_candidates.json',
        'incumbent_scraped_elections.json',
        'scraped_incumbents.json',
        'proposition_scraped_elections.json',
        'scraped_propositions.json',
    ]

    def test_commands(self):
        """
        Run the data loading and processing commands.
        """
        with self.assertRaises(CommandError):
            call_command("processcalaccessdata", verbosity=3, noinput=True)
        call_command("updatecalaccessrawdata", verbosity=3, test_data=True, noinput=True)
        call_command("processcalaccessdata", verbosity=3, noinput=True)

    def test_base_command(self):
        """
        Test options on base commands.
        """
        c = CalAccessCommand()
        c.handle()
        c.header("")
        c.log("")
        c.success("")
        c.warn("")
        c.failure("")
        c.duration()
