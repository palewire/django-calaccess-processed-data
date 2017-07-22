#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filing-related models, managers and mixins.
"""
from time import sleep
import requests


class FilingMixin(object):
    """
    Mixin to add custom methods and properties to Filing objects.
    """
    @property
    def pdf_url(self):
        """
        Returns the url for pdf of the most recent version of the CAL-ACCESS filing.
        """
        return 'http://cal-access.sos.ca.gov/PDFGen/pdfgen.prg?filingid={0}&amendid={1}'.format(
            self.filing_id,
            self.amendment_count
        )

    @property
    def has_pdf(self):
        """
        Make a HEAD request filing's pdf, return True if response status code is 200.

        Pause for half a second before making the request.
        """
        sleep(0.5)

        r = requests.head(self.pdf_url)

        return r.status_code == 200


class FilingVersionMixin(object):
    """
    Mixin to add custom methods and properties to FilingVersion objects.
    """
    @property
    def pdf_url(self):
        """
        Returns the url for pdf of the version of the CAL-ACCESS filing.
        """
        return 'http://cal-access.sos.ca.gov/PDFGen/pdfgen.prg?filingid={0}&amendid={1}'.format(
            self.filing.filing_id,
            self.amend_id
        )

    @property
    def has_pdf(self):
        """
        Make a HEAD request filing version's pdf, return True if response status code is 200.

        Pause for half a second before making the request.
        """
        sleep(0.5)

        r = requests.head(self.pdf_url)

        return r.status_code == 200
