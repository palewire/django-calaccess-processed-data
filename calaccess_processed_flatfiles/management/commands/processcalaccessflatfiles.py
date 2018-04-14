#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load OCD elections models with data extracted and scraped from CAL-ACCESS.
"""
import os
from django.apps import apps
from django.conf import settings
from django.utils.timezone import now
from django.core.management import call_command
from calaccess_processed.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Archive flat files of CAL-ACCESS data.
    """
    help = 'Archive flat files of CAL-ACCESS data'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        # archive if django project setting enabled
        if not getattr(settings, 'CALACCESS_STORE_ARCHIVE', False):
            self.log("Archiving is deactivated. Check your CALACCESS_STORE_ARCHIVE setting.")
            return

        # then archive
        if self.verbosity > 2:
            self.log(' Archiving OCD processed data files.')

        # Get the tracking model instance for this version
        self.processed_version = self.get_or_create_processed_version()[0]

        # create subdirectory in processed_data_dir, if missing
        filings_data_path = os.path.join(self.processed_data_dir, 'flat')
        os.path.isdir(filings_data_path) or os.makedirs(filings_data_path)

        # now do flat files
        flat_file_list = apps.get_app_config("calaccess_processed_flatfiles").get_flat_names_list()
        for f in flat_file_list:
            processed_data_file, created = self.processed_version.files.get_or_create(file_name=f)
            processed_data_file.process_start_datetime = now()
            processed_data_file.save()

            call_command('archivecalaccessflatfile', f)
            processed_data_file.refresh_from_db()
            processed_data_file.process_finish_datetime = now()
            processed_data_file.save()

        # Wrap it up
        self.success('Done!')
