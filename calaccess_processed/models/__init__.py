#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the models from submodules and thread them together.
"""
from calaccess_processed.models.campaign import (
    Candidate,
    F460Summary,
)
from calaccess_processed.models.scraped import (
    ScrapedElection,
    ScrapedCandidate,
    ScrapedCommittee,
    ScrapedProposition,
)
from calaccess_processed.models.common import (
    FilerIDValue,
    FilingIDValue,
)
from calaccess_processed.models.tracking import (
    ProcessedDataVersion,
    ProcessedDataFile,
)

__all__ = (
    'ProcessedDataVersion',
    'ProcessedDataFile',
    'Candidate',
    'F460Summary',
    'ScrapedElection',
    'ScrapedCandidate',
    'ScrapedCommittee',
    'ScrapedProposition',
    'FilerIDValue',
    'FilingIDValue',
)
