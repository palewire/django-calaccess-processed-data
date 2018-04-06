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
from calaccess_processed.management.commands import LoadOCDElectionsBase


class Command(LoadOCDElectionsBase):
    """
    Load OCD elections models with data extracted and scraped from CAL-ACCESS.
    """
    help = 'Load OCD elections models with data extracted and scraped from CAL-ACCESS'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        # Get the tracking model instance for this version
        self.processed_version = self.get_or_create_processed_version()[0]

        # create subdirectory in processed_data_dir, if missing
        filings_data_path = os.path.join(self.processed_data_dir, 'relational')
        os.path.isdir(filings_data_path) or os.makedirs(filings_data_path)
        filings_data_path = os.path.join(self.processed_data_dir, 'flat')
        os.path.isdir(filings_data_path) or os.makedirs(filings_data_path)

        # Start off loading all the data
        self.load()

        # archive if django project setting enabled
        if getattr(settings, 'CALACCESS_STORE_ARCHIVE', False):
            # then archive
            if self.verbosity > 2:
                self.log(' Archiving OCD processed data files.')
            self.archive()
            self.duration()

        # Wrap it up
        self.success('Done!')

    def load(self):
        """
        Load all of the processed models.
        """
        # Set options for commands
        options = dict(verbosity=self.verbosity, no_color=self.no_color)

        #
        # Load parties
        #

        call_command('loadocdparties', **options)
        self.duration()

        #
        # Load elections
        #

        call_command('loadocdballotmeasureelections', **options)
        self.duration()

        call_command('loadocdcandidateelections', **options)
        self.duration()

        #
        # Load contests and candidates
        #

        call_command('loadocdcandidatecontests', **options)
        self.duration()

        call_command('loadocdballotmeasurecontests', **options)
        self.duration()

        call_command('loadocdretentioncontests', **options)
        self.duration()

        call_command('loadocdcandidaciesfrom501s', **options)
        self.duration()

        call_command('loadocdincumbentofficeholders', **options)
        self.duration()

        #
        # Merge duplicates
        #

        call_command('mergeocdpersonsbyfilerid', **options)
        self.duration()

        call_command('mergeocdpersonsbycontestandname', **options)
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
                m._meta.object_name,
            )
            processed_data_file.refresh_from_db()
            processed_data_file.process_finish_datetime = now()
            processed_data_file.save()

        # now do flat files
        flat_file_list = [
            'Candidates', 'BallotMeasures', 'RecallMeasures'
        ]
        for f in flat_file_list:
            processed_data_file, created = self.processed_version.files.get_or_create(
                file_name=f,
            )
            processed_data_file.process_start_datetime = now()
            processed_data_file.save()

            call_command('archivecalaccessprocessedfile', f)
            processed_data_file.refresh_from_db()
            processed_data_file.process_finish_datetime = now()
            processed_data_file.save()
