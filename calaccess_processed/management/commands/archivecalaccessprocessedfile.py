#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Export and archive a .csv file for a given model.
"""
import os
import shutil
import tempfile
from django.apps import apps
from django.core.files import File
from django.db import connection
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
        self.temp_path = os.path.join(
            tempfile.gettempdir(),
            '%s.csv' % self.model_name,
        )
        self.csv_path = os.path.join(
            self.processed_data_dir,
            '%s.csv' % self.model_name,
        )

        # get model
        self.model = apps.get_model(self.app_name, self.model_name)

        # and the db table name
        self.db_table = self.model._meta.db_table

        # Log out what we're doing
        self.log(" Archiving %s.csv" % self.model._meta.object_name)

        # get the current version
        self.version = ProcessedDataVersion.objects.latest('process_start_datetime')

        # and the processed file object
        try:
            self.processed_file = self.version.files.get(file_name=self.model_name)
        except ProcessedDataFile.DoesNotExist:
            self.processed_file = self.version.files.create(
                file_name=self.model_name,
                records_count=self.model.objects.count(),
            )

        # Remove previous .CSV files
        self.processed_file.file_archive.delete()

        # Write out to the temp directory
        with connection.cursor() as c:
            copy_sql = "COPY {db_table} TO '{temp_path}' CSV HEADER;".format(**self.__dict__)
            c.execute(copy_sql)

        # Move the file to the csv directory
        shutil.copy2(self.temp_path, self.csv_path)

        # Open up the .CSV file for reading so we can wrap it in the Django File obj
        with open(self.csv_path, 'rb') as csv_file:
            # Save the .CSV on the raw data file
            self.processed_file.file_archive.save(
                '%s.csv' % self.model_name,
                File(csv_file),
            )

        self.processed_file.file_size = os.path.getsize(self.csv_path)
        self.processed_file.save()
