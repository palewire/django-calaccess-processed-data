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
    from calaccess_processed.models.filings import campaign
    return [
        campaign.form460.Form460FilingVersion,
        campaign.form460.Form460Filing,
        campaign.form460.schedules.a.Form460ScheduleAItemVersion,
        campaign.form460.schedules.a.Form460ScheduleAItem,
        campaign.form460.schedules.b.Form460ScheduleB1ItemVersion,
        campaign.form460.schedules.b.Form460ScheduleB1Item,
        campaign.form460.schedules.b.Form460ScheduleB2ItemVersion,
        campaign.form460.schedules.b.Form460ScheduleB2Item,
        campaign.form460.schedules.b.Form460ScheduleB2ItemVersionOld,
        campaign.form460.schedules.b.Form460ScheduleB2ItemOld,
        campaign.form460.schedules.c.Form460ScheduleCItemVersion,
        campaign.form460.schedules.c.Form460ScheduleCItem,
        campaign.form460.schedules.d.Form460ScheduleDItemVersion,
        campaign.form460.schedules.d.Form460ScheduleDItem,
        campaign.form460.schedules.e.Form460ScheduleEItemVersion,
        campaign.form460.schedules.e.Form460ScheduleEItem,
        campaign.form460.schedules.e.Form460ScheduleESubItemVersion,
        campaign.form460.schedules.e.Form460ScheduleESubItem,
        campaign.form460.schedules.f.Form460ScheduleFItemVersion,
        campaign.form460.schedules.f.Form460ScheduleFItem,
        campaign.form460.schedules.g.Form460ScheduleGItemVersion,
        campaign.form460.schedules.g.Form460ScheduleGItem,
        campaign.form460.schedules.h.Form460ScheduleHItemVersion,
        campaign.form460.schedules.h.Form460ScheduleHItem,
        campaign.form460.schedules.h.Form460ScheduleH2ItemVersionOld,
        campaign.form460.schedules.h.Form460ScheduleH2ItemOld,
        campaign.form460.schedules.i.Form460ScheduleIItemVersion,
        campaign.form460.schedules.i.Form460ScheduleIItem,
        campaign.form501.Form501FilingVersion,
        campaign.form501.Form501Filing,
        campaign.schedule497.Schedule497FilingVersion,
        campaign.schedule497.Schedule497Filing,
        campaign.schedule497.Schedule497Part1ItemVersion,
        campaign.schedule497.Schedule497Part1Item,
        campaign.schedule497.Schedule497Part2ItemVersion,
        campaign.schedule497.Schedule497Part2Item,
    ]


def get_ocd_models_to_load():
    """
    Returns a list of the OCD models with data to be loaded.
    """
    from calaccess_processed.models import opencivicdata

    return [
        opencivicdata.people_orgs.Organization,
        opencivicdata.elections.Election,
        opencivicdata.elections.contest.BallotMeasureContest,
        opencivicdata.elections.candidacy.Candidacy,
        opencivicdata.elections.party.Party,
    ]


def get_ocd_models_to_archive():
    """
    Returns a list of the OCD models with data to be published.
    """
    from calaccess_processed.models import opencivicdata

    return [
        opencivicdata.elections.Election,
        opencivicdata.elections.contest.BallotMeasureContest,
        opencivicdata.elections.candidacy.Candidacy,
        opencivicdata.elections.party.Party,
        opencivicdata.elections.contest.BallotMeasureContest,
        opencivicdata.elections.contest.CandidateContest,
        opencivicdata.elections.candidacy.Candidacy,
        opencivicdata.elections.ballot_selection.BallotMeasureSelection,
        opencivicdata.elections.ballot_selection.CandidateSelection,
        opencivicdata.event.Event,
        opencivicdata.people_orgs.Person,
        opencivicdata.people_orgs.Post,
        opencivicdata.people_orgs.Organization,
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
