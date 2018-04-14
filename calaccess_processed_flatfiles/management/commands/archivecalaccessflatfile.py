#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Export and archive a .csv file for a given model.
"""
from django.apps import apps
from calaccess_processed.management.commands._archivecalaccessprocessedfile import Command as BaseCommand


class Command(BaseCommand):

    def get_model(self, processed_file):
        model_dict = apps.get_app_config("calaccess_processed_flatfiles").get_flat_proxy_lookup()
        return model_dict[processed_file.file_name]
