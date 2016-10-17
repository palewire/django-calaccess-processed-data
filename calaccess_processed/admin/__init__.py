#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the admins from submodules and thread them together.
"""
from calaccess_raw.admin.base import BaseAdmin
from calaccess_processed.admin.campaign import (
    CandidateAdmin,
    CandidateCommitteeAdmin,
    Form460Admin,
    Form460VersionAdmin,
    Schedule497Admin,
    Schedule497VersionAdmin,
    LateContributionReceivedAdmin,
    LateContributionReceivedVersionAdmin,
    LateContributionMadeAdmin,
    LateContributionMadeVersionAdmin,
)
from calaccess_processed.admin.common import (
    FilerIDValueAdmin,
)
from calaccess_processed.admin.tracking import (
    ProcessedDataVersionAdmin,
    ProcessedDataFileAdmin,
)

__all__ = (
    'BaseAdmin',
    'CandidateAdmin',
    'CandidateCommitteeAdmin',
    'Form460Admin',
    'Form460VersionAdmin',
    'Schedule497Admin',
    'Schedule497VersionAdmin',
    'LateContributionReceivedAdmin',
    'LateContributionReceivedVersionAdmin',
    'LateContributionMadeAdmin',
    'LateContributionMadeVersionAdmin',
    'FilerIDValueAdmin',
    'ProcessedDataVersionAdmin',
    'ProcessedDataFileAdmin',
)