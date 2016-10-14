#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the admins from submodules and thread them together.
"""
from calaccess_raw.admin.base import BaseAdmin
from calaccess_processed.admin.campaign import (
    CandidateAdmin,
    CandidateCommitteeAdmin,
    F460FilingAdmin,
    F460FilingVersionAdmin,
    S497FilingAdmin,
    S497FilingVersionAdmin,
    LateContributionReceivedAdmin,
    LateContributionReceivedVersionAdmin,
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
    'F460FilingAdmin',
    'F460FilingVersionAdmin',
    'S497FilingAdmin',
    'S497FilingVersionAdmin',
    'LateContributionReceivedAdmin',
    'LateContributionReceivedVersionAdmin',
    'FilerIDValueAdmin',
    'ProcessedDataVersionAdmin',
    'ProcessedDataFileAdmin',
)