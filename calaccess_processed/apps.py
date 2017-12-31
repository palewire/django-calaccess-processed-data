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
    # Where SQL files are stored in this application
    sql_directory_path = os.path.join(os.path.dirname(__file__), 'sql')
