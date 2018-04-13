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
from . import LoadOCDElectionsBase


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

        # Start off loading all the data
        self.load()

        # archive if django project setting enabled
        if getattr(settings, 'CALACCESS_STORE_ARCHIVE', False):
            # then archive
            if self.verbosity > 2:
                self.log(' Archiving OCD processed data files.')
            self.archive()

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
        models_to_archive = apps.get_app_config("calaccess_processed_elections").get_ocd_models_list()

        for m in models_to_archive:
            obj, created = self.processed_version.files.get_or_create(file_name=m._meta.object_name)
            obj.process_start_datetime = now()
            obj.save()

            call_command('archivecalaccesselectionsfile', m._meta.object_name)
            obj.refresh_from_db()
            obj.process_finish_datetime = now()
            obj.save()
