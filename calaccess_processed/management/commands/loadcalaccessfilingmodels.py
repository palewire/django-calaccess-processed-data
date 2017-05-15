#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load and archive the CAL-ACCESS Filing and FilingVersion models.
"""
from django.apps import apps
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import connection
from django.utils.timezone import now
from calaccess_raw.models.tracking import RawDataVersion
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models.tracking import (
    ProcessedDataVersion,
    ProcessedDataFile,
)


class Command(CalAccessCommand):
    """
    Load and archive the CAL-ACCESS Filing and FilingVersion models.
    """
    help = 'Load and archive the CAL-ACCESS Filing and FilingVersion models.'

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

        # get or create the ProcessedDataVersion instance
        self.processed_version, created = ProcessedDataVersion.objects.get_or_create(
            raw_version=self.raw_version,
        )
        # log if starting or resuming
        if created:
            self.header(
                'Load filings from {:%m-%d-%Y %H:%M:%S} snapshot'.format(
                    self.raw_version.release_datetime
                )
            )
        else:
            self.header(
                'Resume loading of filings from {:%m-%d-%Y %H:%M:%S} snapshot'.format(
                    self.raw_version.release_datetime
                )
            )
        # if there isn't already a process start datetime, set it
        if not self.processed_version.process_start_datetime:
            self.processed_version.process_start_datetime = now()
            self.processed_version.save()

        version_models = [
            m for m in apps.get_app_config('calaccess_processed').get_models()
            if not m._meta.abstract and
            'filings' in str(m) and
            'Version' in str(m)
        ]
        if self.verbosity >= 2:
            self.log(
                " Loading filing %s verison models." % len(version_models)
            )
        self.load_model_list(version_models)

        filing_models = [
            m for m in apps.get_app_config('calaccess_processed').get_models()
            if not m._meta.abstract and
            'filings' in str(m) and
            'Version' not in str(m)
        ]
        if self.verbosity >= 2:
            self.log(
                " Loading filing %s models." % len(filing_models)
            )
        self.load_model_list(filing_models)

        self.processed_version.process_finish_datetime = now()
        self.processed_version.save()

        self.success("Done!")

    def load_model_list(self, model_list):
        """
        Iterate over the given list of models, loading each one.
        """
        # iterate over all of filing models
        for m in model_list:
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
                self.log(" Loading %s" % m._meta.db_table)
            m.objects.load_raw_data()

            processed_file.records_count = m.objects.count()
            processed_file.process_finish_datetime = now()
            processed_file.save()

            call_command(
                'archivecalaccessprocessedfile',
                'calaccess_processed',
                m._meta.object_name,
            )
