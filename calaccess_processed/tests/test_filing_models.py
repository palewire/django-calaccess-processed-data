#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests Filing and FilingVersion models.
"""
from django.test import TestCase
import requests_mock
from calaccess_processed_filings.models import Form460Filing


class Form460FilingTest(TestCase):
    """
    Test for Form460Filing model.
    """
    fixtures = ['form460filing.json', 'form460filingversion.json']

    def test_filing_has_pdf(self):
        """
        Confirm has_pdf returns True for the filing instance.
        """
        filing = Form460Filing.objects.all()[0]
        with requests_mock.Mocker() as m:
            m.register_uri('HEAD', filing.pdf_url)
            self.assertIs(filing.has_pdf, True)

    def test_filing_version_has_pdf(self):
        """
        Confirm has_pdf returns True for the filing instance.
        """
        filing_version = Form460Filing.objects.all()[0].versions.all()[0]
        with requests_mock.Mocker() as m:
            m.register_uri('HEAD', filing_version.pdf_url)
            self.assertIs(filing_version.has_pdf, True)
