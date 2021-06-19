#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Export and archive a .csv file for a given model.
"""
import os
import time
from django.core.files import File
from calaccess_raw import get_data_directory
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models.tracking import ProcessedDataVersion, ProcessedDataFile


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
        parser.add_argument('model_name', help="Name of the model to archive")

    def get_model(self, processed_file):
        """
        Get the model linked to this processed file record.
        """
        raise NotImplementedError

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        # Parse model name
        self.model_name = options['model_name']

        # Log out what we're doing ...
        self.log(" Archiving %s.csv" % self.model_name)

        # ... get the current version ...
        version = ProcessedDataVersion.objects.latest('process_start_datetime')

        # ... and the processed file object ...
        try:
            processed_file = version.files.get(file_name=self.model_name)
        except ProcessedDataFile.DoesNotExist:
            processed_file = version.files.create(file_name=self.model_name)

        # Get the data obj that is paired with the processed_file obj
        data_model = self.get_model(processed_file)

        # Update the records count
        processed_file.records_count = data_model.objects.count()

        # Save it
        processed_file.save()

        # Figure out the path where we will save the file
        csv_dir = os.path.join(
            get_data_directory(),
            'processed',
            data_model().klass_group.lower()
        )
        os.path.exists(csv_dir) or os.mkdir(csv_dir)
        csv_name = '{}.csv'.format(processed_file.file_name)
        csv_path = os.path.join(csv_dir, csv_name)

        # Export a new one
        try:
            copy_to_fields = tuple(i[0] for i in data_model.copy_to_fields)
        except AttributeError:
            copy_to_fields = tuple()
        data_model.objects.to_csv(csv_path, *copy_to_fields)

        # Concoct the Internet Archive identifier
        identifier = "ccdc-processed-data-{dt:%Y-%m-%d_%H-%M-%S}".format(
            dt=version.raw_version.release_datetime
        )

        # Open up the .CSV file for reading so we can wrap it in the Django File obj
        with open(csv_path, 'rb') as csv_file:
            # Save the .CSV on the processed data file
            processed_file.file_archive.save(identifier, File(csv_file))

        # Sleep
        time.sleep(0.5)

        # Save it to the model
        processed_file.file_size = os.path.getsize(csv_path)
        processed_file.save()
