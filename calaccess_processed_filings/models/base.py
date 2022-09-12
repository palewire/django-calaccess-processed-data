"""Filing-related models, managers and mixins."""
from time import sleep

import requests

from calaccess_processed.proxies import OCDProxyModelMixin
from calaccess_processed.models import CalAccessBaseModel
from calaccess_processed_filings.managers import FilingsManager


class FilingBaseModel(CalAccessBaseModel, OCDProxyModelMixin):
    """
    Base model for all the filings models.
    """

    objects = FilingsManager()

    class Meta:
        """
        Meta model options.
        """

        abstract = True
        app_label = "calaccess_processed_filings"

    @property
    def file_name(self):
        """
        The name for the csv to which the model's contents will be dumped.

        If the model is a flat model proxy, return the model's verbose_name_plural
        in CamelCase. Otherwise, return the object_name of the base_model.
        """
        return self._meta.object_name

    @property
    def pdf_url(self):
        """
        Returns the url for pdf of the most recent version of the CAL-ACCESS filing.
        """
        # If it's a Filing, it will have an amendment count. If it's a Version it will have an amend_id.
        try:
            amendid = getattr(self, "amendment_count")
        except AttributeError:
            amendid = getattr(self, "amend_id")
        return "http://cal-access.sos.ca.gov/PDFGen/pdfgen.prg?filingid={}&amendid={}".format(
            self.filing_id, amendid
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
