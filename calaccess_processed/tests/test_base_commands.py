#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for management commands.
"""
from django.test import TestCase
from calaccess_processed.management.commands import CalAccessCommand


class BaseCommandsTest(TestCase):
    """
    Tests to run with no data loaded.
    """
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
