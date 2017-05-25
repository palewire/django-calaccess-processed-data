#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load data into processed CAL-ACCESS models, archive processed files and ZIP.
"""
import os
from django.core.management import call_command
from django.core.files import File
from django.utils.timezone import now
from calaccess_processed.management.commands import CalAccessCommand
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile


class Command(CalAccessCommand):
    """
    Load data into processed CAL-ACCESS models, archive processed files and ZIP.
    """
    help = 'Load data into processed CAL-ACCESS models, archive processed files and ZIP.'

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
        parser.add_argument(
            "--no-scrape",
            action="store_false",
            dest="scrape",
            default=True,
            help="Skip scraping."
        )

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        self.force_restart = options.get("restart")
        self.scrape = options.get("scrape")

        self.processed_version, created = self.get_or_create_processed_version()

        if self.processed_version.update_completed and not self.force_restart:
            msg_tmp = 'Processing completed at %s.'
            self.success(
                msg_tmp % self.processed_version.release_datetime.ctime()
            )
        else:
            # start the clock if created (or restart if forcing restart)
            if created or self.force_restart:
                self.processed_version.processed_start_datetime = now()
                # scrape only if not skipping
                # and either forcing restart or no models loaded yet
            if (
                self.scrape and (
                    self.force_restart or
                    self.processed_version.files.count() == 0
                )
            ):
                self.scrape_all()
            # then load
            self.load()
            # then zip
            self.zip()

            self.success('Processing complete')
            self.duration()

    def scrape_all(self):
        """
        Run all of the CAL-ACCESS scrapers.
        """
        call_command(
            'scrapecalaccesspropositions',
            verbosity=self.verbosity,
            no_color=self.no_color,
            force_flush=True,
        )
        call_command(
            'scrapecalaccesscandidates',
            verbosity=self.verbosity,
            no_color=self.no_color,
            force_flush=True,
        )
        call_command(
            'scrapecalaccessincumbents',
            verbosity=self.verbosity,
            no_color=self.no_color,
            force_flush=True,
        )

    def load(self):
        """
        Load all of the processed models.
        """
        call_command(
            'loadcalaccessfilingmodels',
            verbosity=self.verbosity,
            no_color=self.no_color,
            force_restart=self.force_restart
        )
        self.duration()

        call_command(
            'loadocdmodels',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )
        self.duration()

    def zip(self):
        """
        Zip up all processed data files and archive the zip.
        """
        if self.verbosity:
            self.header("Zipping processed files")
        # Remove previous zip file
        self.processed_version.zip_archive.delete()
        zip_path = os.path.join(self.data_dir, 'processed.zip')

        # enable zipfile compression
        compression = ZIP_DEFLATED

        try:
            zf = ZipFile(zip_path, 'w', compression, allowZip64=True)
        except RuntimeError:
            self.error('Zip file cannot be compressed (check zlib module).')
            compression = ZIP_STORED
            zf = ZipFile(zip_path, 'w', compression, allowZip64=True)

        # loop over and save files in csv dir
        for f in os.listdir(self.processed_data_dir):
            if self.verbosity > 2:
                self.log(" Adding %s to zip" % f)
            csv_path = os.path.join(self.processed_data_dir, f)
            zf.write(csv_path, f)

        # close the zip file
        zf.close()
        if self.verbosity > 2:
            self.log(" All files zipped")

        # save the zip size
        self.processed_version.zip_size = os.path.getsize(zip_path)
        with open(zip_path, 'rb') as zf:
            # Save the zip on the processed data version
            if self.verbosity > 2:
                self.log(" Archiving zip")
            self.processed_version.zip_archive.save(
                os.path.basename(zip_path), File(zf)
            )
        if self.verbosity > 2:
            self.log(" Zip archived.")
