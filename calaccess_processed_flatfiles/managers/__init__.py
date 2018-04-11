#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the managers from submodules and thread them together.
"""
from .ballotmeasurecontests import OCDFlatBallotMeasureContestManager
from .candidacies import OCDFlatCandidacyManager
from .retentioncontests import OCDFlatRetentionContestManager


__all__ = (
    "OCDFlatBallotMeasureContestManager",
    "OCDFlatCandidacyManager",
    "OCDFlatRetentionContestManager",
)
