#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load data extracted from scrape and raw data snapshot into OCD models.
"""
from django.apps import apps
from django.conf import settings
from django.utils.timezone import now
from django.core.management import call_command
from calaccess_processed.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Load data extracted from scrape and raw data snapshot into OCD models.
    """
    help = 'Load data extracted from scrape and raw data snapshot into OCD models'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        self.processed_version = self.get_or_create_processed_version()[0]

        self.load()
        # archive if django project setting enabled
        if getattr(settings, 'CALACCESS_STORE_ARCHIVE', False):
            self.archive()

        self.success('Done!')
        self.duration()

    def load(self):
        """
        Load all of the processed models.
        """
        call_command(
            'loadparties',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )
        self.duration()

        call_command(
            'loadballotmeasurecontests',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )
        self.duration()

        call_command(
            'loadretentioncontests',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )
        self.duration()

        call_command(
            'loadcandidatecontests',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )
        self.duration()

        call_command(
            'mergepersonsbyfilerid',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )
        self.duration()

        call_command(
            'loadcandidaciesfrom501s',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )
        self.duration()

        call_command(
            'mergepersonsbycontestandname',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )
        self.duration()

        call_command(
            'loadincumbentofficeholders',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )
        self.duration()

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
                m._meta.app_label,
                m._meta.object_name,
            )
            processed_data_file.refresh_from_db()
            processed_data_file.process_finish_datetime = now()
            processed_data_file.save()
