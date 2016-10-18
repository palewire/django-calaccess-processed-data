#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the models from submodules and thread them together.
"""
from calaccess_processed.models.campaign import (
    Candidate,
    CandidateCommittee,
    F460Filing,
    F460FilingVersion,
)
from calaccess_processed.models.scraped import (
    CandidateScrapedElection,
    PropositionScrapedElection,
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
    'Candidate',
    'CandidateCommittee',
    'F460Filing',
    'F460FilingVersion',
    'CandidateScrapedElection',
    'PropositionScrapedElection',
    'ScrapedCandidate',
    'ScrapedCommittee',
    'ScrapedProposition',
    'FilerIDValue',
    'FilingIDValue',
    'ProcessedDataVersion',
    'ProcessedDataFile',
)
