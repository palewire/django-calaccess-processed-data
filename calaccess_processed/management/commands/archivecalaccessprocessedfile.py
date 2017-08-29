#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Export and archive a .csv file for a given model.
"""
import os
from django.core.files import File
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
            'model_name',
            help="Name of the model to archive"
        )

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.model_name = options['model_name']

        # Log out what we're doing
        self.log(" Archiving %s.csv" % self.model_name)

        # get the current version
        self.version = ProcessedDataVersion.objects.latest('process_start_datetime')

        # and the processed file object
        processed_file = self.get_processed_file(self.model_name)

        # then archive
        self.archive(processed_file)

    def get_processed_file(self, file_name):
        """
        Return a ProcessedFile object.
        """
        # get model
        try:
            processed_file = self.version.files.get(file_name=file_name)
        except ProcessedDataFile.DoesNotExist:
            processed_file = self.version.files.create(
                file_name=file_name,
            )
        finally:
            # update the records count
            processed_file.update_records_count()

        return processed_file

    def archive(self, processed_file):
        """
        Write the .csv file and upload a copy to the archive.
        """
        # Remove previous .CSV files
        processed_file.file_archive.delete()

        # Export a new one
        processed_file.make_csv_copy()

        # Open up the .CSV file for reading so we can wrap it in the Django File obj
        with open(processed_file.csv_path, 'rb') as csv_file:
            # Save the .CSV on the processed data file
            processed_file.file_archive.save(
                '%s.csv' % self.model_name,
                File(csv_file),
            )

        # Save it to the model
        processed_file.file_size = os.path.getsize(processed_file.csv_path)
        processed_file.save()

        return
