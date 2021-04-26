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
    default_auto_field = 'django.db.models.AutoField'

    # Where SQL files are stored in this application
    sql_directory_path = os.path.join(os.path.dirname(__file__), 'sql')

    def get_filing_model_lookup(self):
        """
        Returns a dictionary with the names mapped to models.
        """
        return dict((m.__name__, m) for m in self.get_filing_models())

    def get_filing_models(self):
        """
        Returns models from the "filings" group that mirror the structure of CAL-ACCESS forms.
        """
        # Get all the models for this app
        model_list = self.get_models()

        # Filter out any abstract ones
        model_list = [m for m in model_list if not m._meta.abstract]

        # Filter out any proxies
        model_list = [m for m in model_list if not m._meta.proxy]

        # Filter down to just models with "filing" in the name
        model_list = [m for m in model_list if 'filings' in str(m)]

        # Return what's left
        return model_list
