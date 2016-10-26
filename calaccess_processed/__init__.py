#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
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
        campaign.filings.Form460Version,
        campaign.filings.Form460,
        campaign.contributions.MonetaryContributionVersion,
        campaign.contributions.MonetaryContribution,
        campaign.contributions.NonMonetaryContribution,
        campaign.contributions.NonMonetaryContributionVersion,
        campaign.contributions.MiscCashIncreaseVersion,
        campaign.contributions.MiscCashIncrease,
        campaign.filings.Schedule497Version,
        campaign.filings.Schedule497,
        campaign.contributions.LateContributionReceivedVersion,
        campaign.contributions.LateContributionReceived,
        campaign.contributions.LateContributionMadeVersion,
        campaign.contributions.LateContributionMade,
    ]

def archive_directory_path(instance, filename):
    """
    Returns a path to an archived processed data file or zip
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
