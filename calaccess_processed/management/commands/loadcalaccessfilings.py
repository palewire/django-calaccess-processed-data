#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load and archive the CAL-ACCESS Filing and FilingVersion models.
"""
import os
from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.db import connection
from django.utils.timezone import now
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models.tracking import ProcessedDataFile


class Command(CalAccessCommand):
    """
    Load and archive the CAL-ACCESS Filing and FilingVersion models.
    """
    help = 'Load and archive the CAL-ACCESS Filing and FilingVersion models.'

    def add_arguments(self, parser):
        """
        Adds custom arguments specific to this command.
        """
        parser.add_argument(
            "--force-restart",
            "--restart",
            action="store_true",
            dest="restart",
            default=False,
            help="Force re-start (overrides auto-resume)."
        )

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        self.force_restart = options.get("restart")

        # get or create the ProcessedDataVersion instance
        self.processed_version, created = self.get_or_create_processed_version()

        if self.processed_version.files.count() > 0 and not self.force_restart:
            self.header(
                'Resume loading of filings from {:%m-%d-%Y %H:%M:%S} snapshot'.format(
                    self.processed_version.raw_version.release_datetime,
                )
            )
        else:
            self.header(
                'Load filings from {:%m-%d-%Y %H:%M:%S} snapshot'.format(
                    self.processed_version.raw_version.release_datetime
                )
            )
        # set the time if not there already or forcing restart
        if not self.processed_version.process_start_datetime or self.force_restart:
            self.processed_version.process_start_datetime = now()
            self.processed_version.save()

        # create subdirectory in processed_data_dir, if missing
        filings_data_path = os.path.join(self.processed_data_dir, 'filings')
        os.path.isdir(filings_data_path) or os.makedirs(filings_data_path)

        self.handle_models('version')
        self.handle_models('filing')

        self.success("Done!")

    def get_model_list(self, model_type):
        """
        Return a list of models of the specified type to be loaded.

        model_type must be "version" of "filing".
        """
        non_abstract_models = [
            m for m in apps.get_app_config('calaccess_processed').get_models()
            if not m._meta.abstract and
            'filings' in str(m)
        ]

        if model_type == 'version':
            models_to_load = [
                m for m in non_abstract_models if 'Version' in str(m)
            ]
        elif model_type == 'filing':
            models_to_load = [
                m for m in non_abstract_models if 'Version' not in str(m)
            ]
        else:
            raise ValueError('model_type must be "version" or "filing".')

        # if not forcing a restart, filter out the models already loaded
        if not self.force_restart:
            loaded_models_q = ProcessedDataFile.objects.filter(
                version=self.processed_version,
                process_finish_datetime__isnull=False,
            )
            if model_type == 'version':
                loaded_models_q.filter(file_name__icontains='Version')
            elif model_type == 'filing':
                loaded_models_q.filter(
                    file_name__icontains='Form'
                ).exclude(file_name__icontains='Version')

            loaded_models = [i.file_name for i in loaded_models_q.all()]

            if self.verbosity >= 2:
                self.log(
                    " {0} {1} models already loaded.".format(
                        len(loaded_models),
                        model_type,
                    )
                )
            models_to_load = [
                m for m in models_to_load
                if m._meta.object_name not in loaded_models
            ]

        return models_to_load

    def load_model_list(self, model_list):
        """
        Iterate over the given list of models, loading each one.
        """
        # iterate over all of filing models
        for m in model_list:
            # set up the ProcessedDataFile instance
            processed_file, created = ProcessedDataFile.objects.get_or_create(
                version=self.processed_version,
                file_name=m._meta.object_name,
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

            # archive if django project setting enabled
            if getattr(settings, 'CALACCESS_STORE_ARCHIVE', False):
                call_command(
                    'archivecalaccessprocessedfile',
                    m._meta.object_name,
                )

    def handle_models(self, model_type):
        """
        Handle logic for loading models of model_type.
        """
        models = self.get_model_list(model_type)
        if len(models) > 0:
            if self.verbosity >= 2:
                self.log(
                    " Loading {0} {1} models.".format(len(models), model_type)
                )
            self.load_model_list(models)
