#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the admins from submodules and thread them together.
"""
from calaccess_raw.admin.base import BaseAdmin
from calaccess_processed.admin.campaign import (
    CandidateAdmin,
    F460SummaryAdmin,
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
    'F460SummaryAdmin',
    'FilerIDValueAdmin',
    'ProcessedDataVersionAdmin',
    'ProcessedDataFileAdmin',
)