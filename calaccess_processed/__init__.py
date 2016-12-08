#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
General utilities for the application.
"""
default_app_config = 'calaccess_processed.apps.CalAccessProcessedConfig'


def get_models_to_process():
    """
    Returns a list of models to derive from raw CAL-ACCESS data.

    Models are listed in the order in which they should be derived, as some
    of data tables derived earlier in the order are re-used in the load queries
    of models later in the order.
    """
    from calaccess_processed.models import campaign
    return [
        campaign.entities.Candidate,
        campaign.entities.CandidateCommittee,
        campaign.filings.form460.Form460FilingVersion,
        campaign.filings.form460.Form460Filing,
        campaign.filings.form460.schedules.a.Form460ScheduleAItemVersion,
        campaign.filings.form460.schedules.a.Form460ScheduleAItem,
        campaign.filings.form460.schedules.b.Form460ScheduleB1ItemVersion,
        campaign.filings.form460.schedules.b.Form460ScheduleB1Item,
        campaign.filings.form460.schedules.b.Form460ScheduleB2ItemVersion,
        campaign.filings.form460.schedules.b.Form460ScheduleB2Item,
        campaign.filings.form460.schedules.b.Form460ScheduleB2ItemVersionOld,
        campaign.filings.form460.schedules.b.Form460ScheduleB2ItemOld,
        campaign.filings.form460.schedules.c.Form460ScheduleCItemVersion,
        campaign.filings.form460.schedules.c.Form460ScheduleCItem,
        campaign.filings.form460.schedules.d.Form460ScheduleDItemVersion,
        campaign.filings.form460.schedules.d.Form460ScheduleDItem,
        campaign.filings.form460.schedules.e.Form460ScheduleEItemVersion,
        campaign.filings.form460.schedules.e.Form460ScheduleEItem,
        campaign.filings.form460.schedules.e.Form460ScheduleESubItemVersion,
        campaign.filings.form460.schedules.e.Form460ScheduleESubItem,
        campaign.filings.form460.schedules.f.Form460ScheduleFItemVersion,
        campaign.filings.form460.schedules.f.Form460ScheduleFItem,
        campaign.filings.form460.schedules.g.Form460ScheduleGItemVersion,
        campaign.filings.form460.schedules.g.Form460ScheduleGItem,
        campaign.filings.form460.schedules.h.Form460ScheduleHItemVersion,
        campaign.filings.form460.schedules.h.Form460ScheduleHItem,
        campaign.filings.form460.schedules.h.Form460ScheduleH2ItemVersionOld,
        campaign.filings.form460.schedules.h.Form460ScheduleH2ItemOld,
        campaign.filings.form460.schedules.i.Form460ScheduleIItemVersion,
        campaign.filings.form460.schedules.i.Form460ScheduleIItem,
        campaign.filings.schedule497.Schedule497FilingVersion,
        campaign.filings.schedule497.Schedule497Filing,
        campaign.filings.schedule497.Schedule497Part1ItemVersion,
        campaign.filings.schedule497.Schedule497Part1Item,
        campaign.filings.schedule497.Schedule497Part2ItemVersion,
        campaign.filings.schedule497.Schedule497Part2Item,
        campaign.elections.Election,
        campaign.propositions.Proposition,
        campaign.propositions.PropositionCommittee
    ]


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
