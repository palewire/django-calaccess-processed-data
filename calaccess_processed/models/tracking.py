#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for tracking processing of CAL-ACCESS snapshots over time.
"""
from __future__ import unicode_literals
from django.db import models
from hurry.filesize import size as sizeformat
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed import archive_directory_path


@python_2_unicode_compatible
class ProcessedDataVersion(models.Model):
    """
    A version of CAL-ACCESS processed data.
    """
    raw_version = models.OneToOneField(
        'calaccess_raw.RawDataVersion',
        related_name='processed_versions',
        verbose_name='raw data version',
        help_text='Foreign key referencing the raw data version processed'
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
    zip_archive = models.FileField(
        blank=True,
        max_length=255,
        upload_to=archive_directory_path,
        verbose_name='cleaned files zip archive',
        help_text='An archive zip of processed files'
    )
    zip_size = models.BigIntegerField(
        null=True,
        verbose_name='zip of size (in bytes)',
        help_text='The expected size (in bytes) of the zip of processed files'
    )

    class Meta:
        """
        Meta model options.
        """
        app_label = 'calaccess_processed'
        verbose_name = 'CAL-ACCESS processed data version'
        ordering = ('-process_start_datetime',)
        get_latest_by = 'process_start_datetime'

    def __str__(self):
        return str(self.raw_version.release_datetime)

    def pretty_zip_size(self):
        """
        Returns a prettified version (e.g., "725M") of the zip's size.
        """
        if not self.zip_size:
            return None
        return sizeformat(self.clean_zip_size)
    pretty_zip_size.short_description = 'processed zip size'
    pretty_zip_size.admin_order_field = 'processed zip size'


@python_2_unicode_compatible
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
        verbose_name='clean records count',
        help_text='Count of records in the processed file'
    )
    file_archive = models.FileField(
        blank=True,
        max_length=255,
        upload_to=archive_directory_path,
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
        verbose_name = 'processd CAL-ACCESS data file'
        ordering = ('-version_id', 'file_name',)

    def __str__(self):
        return self.file_name

    def pretty_file_size(self):
        """
        Returns a prettified version (e.g., "725M") of the processed file's
        size.
        """
        return sizeformat(self.file_size)
    pretty_file_size.short_description = 'processed file size'
    pretty_file_size.admin_order_field = 'processed file size'
