#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load data into processed CAL-ACCESS models, archive processed files and ZIP.
"""
import os
from django.conf import settings
from django.core.files import File
from django.utils.timezone import now
from django.core.management import call_command
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models import ProcessedDataZip


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

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        # Set options
        super(Command, self).handle(*args, **options)
        self.force_restart = options.get("restart")

        # Get or create the logger record
        self.processed_version, created = self.get_or_create_processed_version()

        # If the version is already fully processed and we're not forcing a do-over
        # then just quit out now
        if self.processed_version.update_completed and not self.force_restart:
            msg_tmp = 'Processing completed at %s.'
            self.success(
                msg_tmp % self.processed_version.process_finish_datetime.ctime()
            )
            return False

        # Otherwise proceed with the standard routine
        # First, start the clock if created (or restart if forcing restart)
        if created or self.force_restart:
            self.processed_version.process_start_datetime = now()
            # also reset finish time if forcing re-start
            if self.force_restart:
                self.processed_version.process_finish_datetime = None
            self.processed_version.save()
            if self.verbosity > 2:
                self.log('Flushing local copies of processed data files.')
            self.flush_data_files()

        # then load
        self.load()

        # then verify
        call_command(
            'verifycalaccessprocesseddata',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )

        # then zip
        flat_zip_path = self.zip('flat')
        relational_zip_path = self.zip('relational')

        # then archive
        if getattr(settings, 'CALACCESS_STORE_ARCHIVE', False):
            self.archive_zip(flat_zip_path)
            self.archive_zip(relational_zip_path)

        # Wrap up the log
        self.processed_version.process_finish_datetime = now()
        self.processed_version.save()
        self.success('Processing complete')
        self.duration()

    def flush_data_files(self):
        """
        Delete files in processed_data_dir, prior to archiving.
        """
        for dirpath, dirnames, filenames in os.walk(self.processed_data_dir):
            file_paths = [os.path.join(dirpath, i) for i in filenames]
            for file_path in file_paths:
                try:
                    os.remove(file_path)
                except OSError:
                    pass

    def load(self):
        """
        Load all of the processed models.
        """
        call_command(
            'loadcalaccessfilings',
            verbosity=self.verbosity,
            no_color=self.no_color,
            force_restart=self.force_restart
        )
        self.duration()

        call_command(
            'loadocdelections',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )
        self.duration()

    def zip(self, directory_name):
        """
        Zip up files in directory_name (in processed_data_dir).
        """
        directory = os.path.join(self.processed_data_dir, directory_name)
        if self.verbosity:
            self.log("Zipping files in %s/" % directory)

        # enable zipfile compression
        compression = ZIP_DEFLATED
        zip_path = os.path.join(self.data_dir, '%s.zip' % directory_name)

        try:
            zf = ZipFile(zip_path, 'w', compression, allowZip64=True)
        except RuntimeError:
            self.error('Zip file cannot be compressed (check zlib module).')
            compression = ZIP_STORED
            zf = ZipFile(zip_path, 'w', compression, allowZip64=True)

        # loop over and save files in csv processed data dir
        for f in os.listdir(directory):
            if self.verbosity > 2:
                self.log(" Adding %s to zip" % f)
            csv_path = os.path.join(directory, f)
            zf.write(csv_path, f)

        # close the zip file
        zf.close()

        return zip_path

    def archive_zip(self, zip_path):
        """
        Archive the zip.
        """
        zip_name = os.path.basename(zip_path)
        try:
            zip_obj = self.processed_version.zips.get(
                zip_archive__icontains=zip_name.split('.')[0]
            )
        except ProcessedDataZip.DoesNotExist:
            zip_obj = self.processed_version.zips.create()
        else:
            if self.verbosity > 2:
                self.log(" Deleting previous archive of %s" % zip_name)
            zip_obj.zip_archive.delete()

        with open(zip_path, 'rb') as zf:
            # Save the zip on the processed data version
            if self.verbosity > 2:
                self.log(" Archiving %s" % zip_name)
            zip_obj.zip_archive.save(zip_name, File(zf))

        # update the zip size
        if zip_obj.zip_size != os.path.getsize(zip_path):
            zip_obj.zip_size = os.path.getsize(zip_path)
            zip_obj.save()

        if self.verbosity > 2:
            self.log(" %s archived." % zip_name)
