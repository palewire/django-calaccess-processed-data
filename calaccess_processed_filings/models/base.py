#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filing-related models, managers and mixins.
"""
import requests
from time import sleep
from calaccess_processed.models.base import CalAccessBaseModel
from calaccess_processed_filings.managers import FilingsManager


class FilingBaseModel(CalAccessBaseModel):
    """
    Base model for all the filings models.
    """
    objects = FilingsManager()

    class Meta:
        """
        Meta model options.
        """
        abstract = True
        app_label = 'calaccess_processed_filings'

    @property
    def pdf_url(self):
        """
        Returns the url for pdf of the most recent version of the CAL-ACCESS filing.
        """
        return 'http://cal-access.sos.ca.gov/PDFGen/pdfgen.prg?filingid={}&amendid={}'.format(
            self.filing_id,
            # If it's a Filing, it will have an amendment count. If it's a Version it will have an amend_id.
            getattr(self, 'amendment_count', getattr('self', 'amend_id'))
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
