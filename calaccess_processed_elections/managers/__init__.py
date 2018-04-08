#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the managers from submodules and thread them together.
"""
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
    "OCDCandidacyQuerySet",
    "OCDCandidacyManager",
    "OCDCandidateContestQuerySet",
    "OCDCandidateContestManager",
    "OCDPartisanPrimaryManager",
    "OCDElectionManager",
    "OCDPartyManager"
)
