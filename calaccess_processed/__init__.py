#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
General utilities for the application.
"""
from __future__ import unicode_literals
default_app_config = 'calaccess_processed.apps.CalAccessProcessedConfig'


def archive_directory_path(instance, filename):
    """
    Returns a path to an archived processed data file or ZIP.
    """
    from .models import ProcessedDataZip, ProcessedDataFile

    if isinstance(instance, ProcessedDataZip):
        release_datetime = instance.version.raw_version.release_datetime
        f_name, f_ext = filename.split('.')
        return '{fn}_{dt:%Y-%m-%d_%H-%M-%S}.{fx}'.format(
            fn=f_name,
            dt=release_datetime,
            fx=f_ext,
        )
    elif isinstance(instance, ProcessedDataFile):
        release_datetime = instance.version.raw_version.release_datetime
        return '{dt:%Y-%m-%d_%H-%M-%S}/{f}'.format(dt=release_datetime, f=filename)
    else:
        raise TypeError("Must be ProcessedDataVersion or ProcessedDataFile instance.")


__all__ = ('archive_directory_path',)
