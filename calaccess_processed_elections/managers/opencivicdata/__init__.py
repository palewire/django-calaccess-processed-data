#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the managers from submodules and thread them together.
"""
from .core import (
    OCDAssemblyDivisionManager,
    OCDSenateDivisionManager,
    OCDCaliforniaDivisionManager,
    OCDJurisdictionManager,
    OCDOrganizationManager,
    OCDMembershipManager,
    OCDPersonManager,
    OCDPostManager,
    OCDAssemblyPostManager,
    OCDExecutivePostManager,
    OCDSenatePostManager,
)
from .elections import (
    OCDCandidacyQuerySet,
    OCDCandidacyManager,
    OCDCandidateContestQuerySet,
    OCDCandidateContestManager,
    OCDPartisanPrimaryManager,
    OCDElectionManager,
    OCDPartyManager,
)


__all__ = (
    "OCDAssemblyDivisionManager",
    "OCDSenateDivisionManager",
    "OCDCaliforniaDivisionManager",
    "OCDJurisdictionManager",
    "OCDOrganizationManager",
    "OCDMembershipManager",
    "OCDPersonManager",
    "OCDPostManager",
    "OCDAssemblyPostManager",
    "OCDExecutivePostManager",
    "OCDSenatePostManager",
    "OCDCandidacyQuerySet",
    "OCDCandidacyManager",
    "OCDCandidateContestQuerySet",
    "OCDCandidateContestManager",
    "OCDPartisanPrimaryManager",
    "OCDElectionManager",
    "OCDPartyManager",
)
