#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic configuration for the application.
"""
from __future__ import unicode_literals
import os
from django.apps import AppConfig


class CalAccessProcessedFilingsConfig(AppConfig):
    """
    Application configuration.
    """
    name = 'calaccess_processed_filings'
    verbose_name = "CAL-ACCESS processed data: Filings"
    # Where SQL files are stored in this application
    sql_directory_path = os.path.join(os.path.dirname(__file__), 'sql')

    def get_concrete_models(self):
        """
        Returns models that are actually in the database and not abstract or a proxy.
        """
        model_list = self.get_models()
        model_list = [m for m in model_list if not m._meta.abstract]
        return [m for m in model_list if not m._meta.proxy]

    def get_filing_models(self):
        """
        Returns models from the "filings" group that mirror the structure of CAL-ACCESS forms.
        """
        model_list = self.get_concrete_models()
        return [m for m in model_list if 'filings' in str(m)]
