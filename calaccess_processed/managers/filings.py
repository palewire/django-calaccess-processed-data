#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom manager for loading raw data in to "filings" models.
"""
from __future__ import unicode_literals
import os
import itertools

# Django tricks
from django.apps import apps
from django.db.models import Q

# Managers
from .bulkloadsql import BulkLoadSQLManager

# Logging
import logging
logger = logging.getLogger(__name__)


class FilingsManager(BulkLoadSQLManager):
    """
    Utilities for more quickly loading bulk data.
    """
    @property
    def sql(self):
        """
        Return string of raw sql for loading the model.
        """
        return open(self.sql_path, 'r').read()

    @property
    def sql_path(self):
        """
        Return the path to the .sql file with the model's loading query.
        """
        file_name = 'filings/load_%s_model' % self.model._meta.model_name
        return self.get_sql_path(file_name)

    def get_sql_path(self, file_name):
        """
        Return the full path with extenstion to file_name.
        """
        return os.path.join(apps.get_app_config("calaccess_processed").sql_directory_path, '%s.sql' % file_name)


class Form501FilingManager(FilingsManager):
    """
    A custom manager for Form 501 filings.
    """
    def without_candidacy(self):
        """
        Returns Form 501 filings that do not have an OCD Candidacy yet.
        """
        OCDCandidacyProxy = apps.get_model("calaccess_processed", "OCDCandidacyProxy")

        matched_qs = OCDCandidacyProxy.objects.matched_form501_ids()
        matched_list = [i for i in itertools.chain.from_iterable(matched_qs)]
        return self.get_queryset().exclude(
            Q(filing_id__in=matched_list) | Q(office__icontains='RETIREMENT')
        )
