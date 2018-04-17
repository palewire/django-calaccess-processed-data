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
        model_dict = apps.get_app_config("calaccess_processed_elections").get_ocd_proxy_lookup()
        return model_dict[processed_file.file_name]
