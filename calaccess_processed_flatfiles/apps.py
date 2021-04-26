#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic configuration for the application.
"""
from __future__ import unicode_literals
import os
import collections
from django.apps import AppConfig


class CalAccessProcessedFlatfilesConfig(AppConfig):
    """
    Application configuration.
    """
    name = 'calaccess_processed_flatfiles'
    verbose_name = "CAL-ACCESS processed data: Flat files"
    default_auto_field = 'django.db.models.AutoField'

    # Where SQL files are stored in this application
    sql_directory_path = os.path.join(os.path.dirname(__file__), 'sql')

    def get_flat_names_list(self):
        """
        Returns a list of all of the flatfile names.
        """
        return list(self.get_flat_proxy_lookup().keys())

    def get_flat_proxy_list(self):
        """
        Returns a list of all the flatfile proxies.
        """
        return list(self.get_flat_proxy_lookup().values())

    def get_flat_proxy_lookup(self):
        """
        Returns a dictionary crosswalk between flatfile names and proxies.
        """
        from . import proxies
        return collections.OrderedDict({
            'Candidates': proxies.OCDFlatCandidacyProxy,
            'BallotMeasures': proxies.OCDFlatBallotMeasureContestProxy,
            'RecallMeasures': proxies.OCDFlatRetentionContestProxy
        })
