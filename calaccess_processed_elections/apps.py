#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic configuration for the application.
"""
from __future__ import unicode_literals
import os
from django.apps import apps
from django.apps import AppConfig


class CalAccessProcessedElectionsConfig(AppConfig):
    """
    Application configuration.
    """
    name = 'calaccess_processed_elections'
    verbose_name = "CAL-ACCESS processed data: Elections"
    # Where SQL files are stored in this application
    sql_directory_path = os.path.join(os.path.dirname(__file__), 'sql')

    def get_archived_models(self):
        """
        Returns a list of the models that should be saved in our archive.
        """
        # Pull the two different OCD lists we want to archive
        ocd_core = apps.get_app_config('core').get_models()
        ocd_elections = apps.get_app_config('elections').get_models()

        # Combine them
        ocd_model_list = list(ocd_core) + list(ocd_elections)

        # Remove any abstract models
        ocd_model_list = [m for m in ocd_model_list if not m._meta.abstract]

        # Remove any models with no records
        ocd_model_list = [m for m in ocd_model_list if m.objects.count() > 0]

        # Return what's left
        return ocd_model_list
