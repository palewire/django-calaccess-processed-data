#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load data extracted from scrape and raw data snapshot into OCD elections models.
"""
from django.apps import apps
from django.conf import settings
from django.utils.timezone import now
from django.core.management import call_command
from calaccess_processed.models import OCDDivisionProxy
from calaccess_processed.management.commands import CalAccessCommand
from opencivicdata.core.management.commands.loaddivisions import load_divisions


class Command(CalAccessCommand):
    """
    Load data extracted from scrape and raw data snapshot into OCD elections models.
    """
    help = 'Load data extracted from scrape and raw data snapshot into OCD elections models.'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        # Get the logger for this version
        self.processed_version = self.get_or_create_processed_version()[0]

        # Start off loading all the data
        self.load()

        # archive if django project setting enabled
        if getattr(settings, 'CALACCESS_STORE_ARCHIVE', False):
            self.archive()

        # Wrap it up
        self.success('Done!')
        self.duration()

    def load(self):
        """
        Load all of the processed models.
        """
        # Verify that OCD divisions have been loaded
        try:
            OCDDivisionProxy.objects.california()
        except OCDDivisionProxy.DoesNotExist:
            if self.verbosity > 2:
                self.log(' CA state division missing. Loading all U.S. divisions')
            load_divisions('us')

        options = dict(
            verbosity=self.verbosity,
            no_color=self.no_color,
        )
        call_command('loadocdparties', **options)
        self.duration()

        call_command('loadocdcandidateelections', **options)
        self.duration()

        call_command('loadocdballotmeasurecontests', **options)
        self.duration()

        call_command('loadocdretentioncontests', **options)
        self.duration()

        call_command('loadocdcandidatecontests', **options)
        self.duration()

        call_command('mergeocdpersonsbyfilerid', **options)
        self.duration()

        call_command('loadocdcandidaciesfrom501s', **options)
        self.duration()

        call_command('mergeocdpersonsbycontestandname', **options)
        self.duration()

        # call_command('loadocdincumbentofficeholders', **options)
        # self.duration()

    def archive(self):
        """
        Save a csv file for each loaded OCD model.
        """
        core_models = [
            m for m in apps.get_app_config('core').get_models()
            if not m._meta.abstract and
            m.objects.count() > 0
        ]

        elections_models = [
            m for m in apps.get_app_config('elections').get_models()
            if not m._meta.abstract and
            m.objects.count() > 0
        ]

        models_to_load = core_models + elections_models

        for m in models_to_load:
            processed_data_file, created = self.processed_version.files.get_or_create(
                file_name=m._meta.object_name,
            )
            processed_data_file.process_start_datetime = now()
            processed_data_file.save()

            call_command(
                'archivecalaccessprocessedfile',
                m._meta.object_name,
            )
            processed_data_file.refresh_from_db()
            processed_data_file.process_finish_datetime = now()
            processed_data_file.save()
