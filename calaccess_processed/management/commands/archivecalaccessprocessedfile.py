#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Export and archive a .csv file for a given model.
"""
import os
from django.apps import apps
from django.conf import settings
from django.core.files import File
from django.db import connection
from calaccess_raw import get_download_directory
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models.tracking import (
    ProcessedDataVersion,
    ProcessedDataFile,
)


class Command(CalAccessCommand):
    """
    Export and archive a .csv file for a given model.
    """
    help = 'Export and archive a .csv file for a given model.'

    def add_arguments(self, parser):
        """
        Adds custom arguments specific to this command.
        """
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            'app_name',
            help="Name of the app with the model"
        )
        parser.add_argument(
            'model_name',
            help="Name of the model to archive"
        )

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.app_name = options['app_name']
        self.model_name = options['model_name']

        # get the full path for archiving the csv
        self.csv_path = os.path.join(
            get_download_directory(),
            'processed',
            '%s.csv' % self.model_name,
        )
        # get model
        self.model = apps.get_model(self.app_name, self.model_name)
        # and the db table name
        self.db_table = self.model._meta.db_table
        # get the processed file object
        try:
            self.processed_file = ProcessedDataFile.objects.filter(
                file_name=self.model_name.lower()
            ).latest('process_finish_datetime')
        except ProcessedDataFile.DoesNotExist:
            self.processed_file = ProcessedDataFile.objects.create(
                file_name=self.model_name.lower(),
                version=ProcessedDataVersion.objects.latest('process_start_datetime')
            )

        if getattr(settings, 'CALACCESS_STORE_ARCHIVE', False):
            if self.verbosity > 2:
                self.log(" Archiving {0}".format(os.path.basename(self.model_name)))
            # Remove previous .CSV and error log files
            self.processed_file.file_archive.delete()

            with connection.cursor() as c:
                c.execute(
                    """
                    COPY {db_table} TO '{csv_path}' CSV HEADER;
                    """.format(**self.__dict__)
                )

            # Open up the .CSV file for reading so we can wrap it in the Django File obj
            with open(self.csv_path, 'rb') as csv_file:
                # Save the .CSV on the raw data file
                self.processed_file.file_archive.save(
                    '%s.csv' % self.model_name,
                    File(csv_file),
                )
