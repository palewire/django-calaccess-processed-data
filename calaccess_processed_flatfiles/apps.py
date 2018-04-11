#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic configuration for the application.
"""
from __future__ import unicode_literals
import os
from django.apps import AppConfig


class CalAccessProcessedFlatfilesConfig(AppConfig):
    """
    Application configuration.
    """
    name = 'calaccess_processed_flatfiles'
    verbose_name = "CAL-ACCESS processed data: Flat files"
    # Where SQL files are stored in this application
    sql_directory_path = os.path.join(os.path.dirname(__file__), 'sql')
