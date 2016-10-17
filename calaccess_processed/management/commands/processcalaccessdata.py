#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load data into processed CAL-ACCESS models, archive processed files and ZIP.
"""
import os
import csv
from django.conf import settings
from django.core.files import File
from django.core.management.base import CommandError
from django.db import connection
from django.utils.timezone import now
from calaccess_raw import get_download_directory
from calaccess_processed import get_models_to_process
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models.tracking import (
    ProcessedDataVersion,
    ProcessedDataFile,
)
from calaccess_raw.models.tracking import RawDataVersion


class Command(CalAccessCommand):
    """ 
    Load data into processed CAL-ACCESS models, archive processed files and ZIP
    """
    help = 'Load data into processed CAL-ACCESS models, archive processed \
files and ZIP.'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        # get the most recently loaded raw data version
        try:
            self.raw_version = RawDataVersion.objects.complete()[0]
        except IndexError:
            raise CommandError(
                'No raw CAL-ACCESS data loaded (run `python manage.py '
                'updatecalaccessrawdata`).'
            )
        # set up processed data directory
        self.processed_data_dir = os.path.join(
            get_download_directory(),
            'processed',
        )
        if not os.path.exists(self.processed_data_dir):
            os.makedirs(self.processed_data_dir)

        # get or create the ProcessedDataVersion instance
        self.processed_version, created = ProcessedDataVersion.objects.get_or_create(
            raw_version = self.raw_version,
        )
        # log if starting or resuming
        if created:
            self.header(
                'Processing {:%m-%d-%Y %H:%M:%S} snapshot'.format(
                    self.raw_version.release_datetime
                )
            )
        else:
            self.header(
                'Resuming processing of {:%m-%d-%Y %H:%M:%S} snapshot'.format(
                    self.raw_version.release_datetime
                )
            )
        # if there isn't already a process start datetime, set it
        if not self.processed_version.process_start_datetime:
            self.processed_version.process_start_datetime = now()
            self.processed_version.save()

        # get all of the models
        self.processed_models = get_models_to_process()

        # iterate over all of the processed models
        for m in self.processed_models:
            # set up the ProcessedDataFile instance
            processed_file, created = ProcessedDataFile.objects.get_or_create(
                version=self.processed_version,
                file_name=m._meta.model_name,
            )
            processed_file.process_start_datetime = now()
            processed_file.save()
            # flush the processed model
            if self.verbosity > 2:
                self.log(" Truncating %s" % m._meta.db_table)
            with connection.cursor() as c:
                c.execute('TRUNCATE TABLE "%s" CASCADE' % (m._meta.db_table))
            # load the processed model
            if self.verbosity > 2:
                self.log(" Loading raw data into %s" % m._meta.db_table)
            m.objects.load_raw_data()
            # export the processed model data
            processed_file_path = os.path.join(
                self.processed_data_dir,
                '%s.csv' % m._meta.model_name,
            )
            if self.verbosity > 2:
                self.log(" Exporting to %s" % processed_file_path)
            with open(processed_file_path, 'wb') as f:
                writer = csv.writer(f)
                # write the header
                headers = []
                for field in m._meta.fields:
                    headers.append(field.name)
                writer.writerow(headers)
                # write the rows
                for obj in m.objects.all():
                    row = []
                    for field in headers:
                        val = getattr(obj, field)
                        if callable(val):
                            val = val()
                        row.append(val)
                    writer.writerow(row)

            # archive the processed file
            if getattr(settings, 'CALACCESS_STORE_ARCHIVE', False):
                if self.verbosity > 2:
                    self.log(" Archiving %s" % processed_file_path)
                # Remove previously archived file
                processed_file.file_archive.delete()
                
                # Add file size to the processed_file
                processed_file.file_size = os.path.getsize(
                    processed_file_path
                ) or 0
                
                # Open up .csv file so we can wrap it in the Django File obj
                with open(processed_file_path) as f:
                    # Save .csv on the processed data file
                    processed_file.file_archive.save(
                        processed_file.file_name + ".csv",
                        File(f),
                    )

            processed_file.records_count = m.objects.count()
            processed_file.process_finish_datetime = now()
            processed_file.save()

        

        self.processed_version.process_finish_datetime = now()
        self.processed_version.save()

        self.success("Done!")
