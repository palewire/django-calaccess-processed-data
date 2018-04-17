#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Export and archive a .csv file for a given model.
"""
from django.apps import apps
from calaccess_processed.management.commands._archivecalaccessprocessedfile import Command as BaseCommand


class Command(BaseCommand):
    """
    A version of the parent command for this app.
    """
    def get_model(self, processed_file):
        """
        Submit a processed_file and receive the proper proxy.
        """
        model_list = apps.get_app_config("calaccess_processed_filings").get_filing_models()
        model_dict = dict((m.__name__, m) for m in model_list)
        return model_dict[processed_file.file_name]
