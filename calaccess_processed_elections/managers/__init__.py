#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the managers from submodules and thread them together.
"""
from .calaccess_raw import RawFilerToFilerTypeCdManager
from .calaccess_processed_elections.managers.calaccess_scraped import (
    ScrapedIncumbentElectionManager,
    ScrapedBallotMeasureManager,
    ScrapedRecallMeasureManager
)
from .candidacies import (
    OCDCandidacyQuerySet,
    OCDCandidacyManager
)
from .candidatecontests import (
    OCDCandidateContestQuerySet,
    OCDCandidateContestManager
)
from .elections import (
    OCDPartisanPrimaryManager,
    OCDElectionManager
)
from .parties import OCDPartyManager


__all__ = (
    "RawFilerToFilerTypeCdManager",
    "ScrapedIncumbentElectionManager",
    "ScrapedBallotMeasureManager",
    "ScrapedRecallMeasureManager",
    "OCDCandidacyQuerySet",
    "OCDCandidacyManager",
    "OCDCandidateContestQuerySet",
    "OCDCandidateContestManager",
    "OCDPartisanPrimaryManager",
    "OCDElectionManager",
    "OCDPartyManager"
)
