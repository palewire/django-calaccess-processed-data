#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
General utilities for the application.
"""
default_app_config = 'calaccess_processed.apps.CalAccessProcessedConfig'


def archive_directory_path(instance, filename):
    """
    Returns a path to an archived processed data file or ZIP.
    """
    from calaccess_processed.models.tracking import (
        ProcessedDataVersion,
        ProcessedDataFile,
    )

    if isinstance(instance, ProcessedDataVersion):
        release_datetime = instance.raw_version.release_datetime
        f_name, f_ext = filename.split('.')
        path = '{fn}_{dt:%Y-%m-%d_%H-%M-%S}.{fx}'.format(
            fn=f_name,
            dt=release_datetime,
            fx=f_ext,
        )
    elif isinstance(instance, ProcessedDataFile):
        release_datetime = instance.version.raw_version.release_datetime
        path = '{dt:%Y-%m-%d_%H-%M-%S}/{f}'.format(dt=release_datetime, f=filename)
    else:
        raise TypeError(
            "Must be ProcessedDataVersion or ProcessedDataFile instance."
        )
    return path
