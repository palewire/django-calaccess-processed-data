#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for this application.
"""
from django.test import TestCase
from calaccess_processed import models
from django.core.management import call_command


class ProcessedDataTest(TestCase):
    """
    Create model objects and try out their attributes.
    """
    @classmethod
    def setUpClass(cls):
        """
        Load data into the database before running other tests.
        """
        super(ProcessedDataTest, cls).setUpClass()
        call_command("updatecalaccessrawdata", verbosity=3, test_data=True, noinput=True)
        call_command("processcalaccessdata", verbosity=3, noinput=True)

    # def test_models(self):
    #     """
    #     Tests the models.
    #     """
    #     self.assertTrue(models.Form460Filing.objects.count() > 0)
