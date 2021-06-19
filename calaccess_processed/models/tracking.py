#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for tracking processing of CAL-ACCESS snapshots over time.
"""
from django.apps import apps
from hurry.filesize import size as sizeformat

# Models
from django.db import models
from ia_storage.fields import InternetArchiveFileField


class ProcessedDataVersion(models.Model):
    """
    A version of CAL-ACCESS processed data.
    """
    raw_version = models.OneToOneField(
        'calaccess_raw.RawDataVersion',
        related_name='processed_version',
        verbose_name='raw data version',
        help_text='Foreign key referencing the raw data version processed',
        on_delete=models.CASCADE
    )
    process_start_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time processing started',
        help_text='Date and time when the processing of the CAL-ACCESS version'
                  ' started',
    )
    process_finish_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time update finished',
        help_text='Date and time when the processing of the CAL-ACCESS version'
                  ' finished',
    )

    class Meta:
        """
        Meta model options.
        """
        app_label = 'calaccess_processed'
        verbose_name = 'TRACKING: CAL-ACCESS processed data version'
        ordering = ('-process_start_datetime',)
        get_latest_by = 'process_start_datetime'

    def __str__(self):
        return str(self.raw_version.release_datetime)

    @property
    def update_completed(self):
        """
        Check if the database update to the version completed.

        Return True or False.
        """
        if self.process_finish_datetime:
            is_completed = True
        else:
            is_completed = False

        return is_completed

    @property
    def update_stalled(self):
        """
        Check if the database update to the version started but did not complete.

        Return True or False.
        """
        if self.process_start_datetime and not self.update_finish_datetime:
            is_stalled = True
        else:
            is_stalled = False

        return is_stalled

    def check_processed_model(self, model):
        """
        Return True if model was processed in this version.
        """
        try:
            file_name = model().file_name
        except AttributeError:
            file_name = model().klass_name
        return self.files.filter(file_name=file_name).exists()


class ProcessedDataZip(models.Model):
    """
    A zip file containing a subset of processed data files for a version.
    """
    version = models.ForeignKey(
        'ProcessedDataVersion',
        on_delete=models.CASCADE,
        related_name='zips',
        verbose_name='processed data version',
        help_text='Foreign key referencing the processed version of CAL-ACCESS'
    )
    zip_archive = InternetArchiveFileField(
        max_length=255,
        verbose_name='zip archive',
        help_text='An archived zip of processed files'
    )
    zip_size = models.BigIntegerField(
        default=0,
        verbose_name='size of zip (in bytes)',
        help_text='The expected size (in bytes) of the zip '
    )
    created_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date and time zip created',
        help_text='Date and time when zip was created',
    )

    class Meta:
        """
        Meta model options.
        """
        app_label = 'calaccess_processed'
        verbose_name = 'TRACKING: CAL-ACCESS processed data zip'
        ordering = ('-version', 'zip_archive')
        unique_together = ('version', 'zip_archive')

    def __str__(self):
        return '{0} ({1})'.format(self.zip_archive, self.version)

    def pretty_zip_size(self):
        """
        Returns a prettified version (e.g., "725M") of the zip's size.
        """
        if not self.zip_size:
            return None
        return sizeformat(self.zip_size)
    pretty_zip_size.short_description = 'processed zip size'
    pretty_zip_size.admin_order_field = 'processed zip size'


class ProcessedDataFile(models.Model):
    """
    A data file included in a processed version of CAL-ACCESS.
    """
    version = models.ForeignKey(
        'ProcessedDataVersion',
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='processed data version',
        help_text='Foreign key referencing the processed version of CAL-ACCESS'
    )
    file_name = models.CharField(
        max_length=100,
        verbose_name='processed data file name',
        help_text='Name of the processed data file without extension',
    )
    process_start_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time processing started',
        help_text='Date and time when the processing of the file started',
    )
    process_finish_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time processing finished',
        help_text='Date and time when the processing of the file finished',
    )
    records_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='records count',
        help_text='Count of records in the processed file'
    )
    file_archive = InternetArchiveFileField(
        blank=True,
        max_length=255,
        verbose_name='archive of processed file',
        help_text='An archive of the processed file'
    )
    file_size = models.BigIntegerField(
        null=False,
        default=0,
        verbose_name='size of processed data file (in bytes)',
        help_text='Size of the processed file (in bytes)'
    )

    class Meta:
        """
        Meta model options.
        """
        app_label = 'calaccess_processed'
        unique_together = (('version', 'file_name'),)
        verbose_name = 'TRACKING: CAL-ACCESS processed data file'
        ordering = ('-version_id', 'file_name',)

    def __str__(self):
        return self.file_name

    def pretty_file_size(self):
        """
        Returns a prettified version (e.g., "725M") of the processed file's size.
        """
        return sizeformat(self.file_size)
    pretty_file_size.short_description = 'processed file size'
    pretty_file_size.admin_order_field = 'processed file size'

    @property
    def is_flat(self):
        """
        Return True if the proxy model is used to flatten relational data models.
        """
        try:
            is_flat = self.model().is_flat
        except (AttributeError, TypeError):
            is_flat = False
        return is_flat

    @property
    def model(self):
        """
        Returns the model associated with this record.
        """
        lookup = apps.get_app_config("calaccess_processed").get_processed_file_lookup()
        return lookup[self.file_name]
