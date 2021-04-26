#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic configuration for the application.
"""
from __future__ import unicode_literals
import os
from django.apps import AppConfig


class CalAccessProcessedConfig(AppConfig):
    """
    Application configuration.
    """
    name = 'calaccess_processed'
    verbose_name = "CAL-ACCESS processed data"
    default_auto_field = 'django.db.models.AutoField'
    # Where SQL files are stored in this application
    sql_directory_path = os.path.join(os.path.dirname(__file__), 'sql')

    def get_processed_file_lookup(self):
        """
        Returns a dictionary with the names of processed files mapped to models.
        """
        from django.apps import apps
        d = {}
        filings = apps.get_app_config("calaccess_processed_filings").get_filing_model_lookup()
        elections = apps.get_app_config("calaccess_processed_elections").get_ocd_proxy_lookup()
        flat = apps.get_app_config("calaccess_processed_flatfiles").get_flat_proxy_lookup()
        d.update(filings)
        d.update(elections)
        d.update(flat)
        return d
