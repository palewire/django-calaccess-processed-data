#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
General utilities for the application.
"""
from __future__ import unicode_literals
from datetime import date
default_app_config = 'calaccess_processed.apps.CalAccessProcessedConfig'


def archive_directory_path(instance, filename):
    """
    Returns a path to an archived processed data file or ZIP.
    """
    from calaccess_processed.models.tracking import (
        ProcessedDataZip,
        ProcessedDataFile,
    )

    if isinstance(instance, ProcessedDataZip):
        release_datetime = instance.version.raw_version.release_datetime
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


def get_expected_election_date(year, election_type):
    """
    Get the date of the election in the given year and type.

    Raise an exception if year is not even or if election_type is not
    "PRIMARY" or "GENERAL".

    Return a date object.
    """
    # Rules defined here:
    # https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=ELEC&division=1.&title=&part=&chapter=1.&article= # noqa
    if year % 2 != 0:
        raise ValueError("Regular elections occur in even years.")
    elif election_type.upper() == 'PRIMARY':
        # Primary elections are in June
        month = 6
    elif election_type.upper() == 'GENERAL':
        # General elections are in November
        month = 11
    else:
        raise ValueError("election_type must 'PRIMARY' or 'GENERAL'.")

    # get the first weekday
    # zero-indexed starting with monday
    first_weekday = date(year, month, 1).weekday()

    # calculate day or first tuesday after first monday
    day_or_month = (7 - first_weekday) % 7 + 2

    return date(year, month, day_or_month)


__all__ = (
    'archive_directory_path',
    'get_expected_election_date',
)
