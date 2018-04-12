#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the managers from submodules and thread them together.
"""
from .calaccess_raw import RawFilerToFilerTypeCdManager
from .calaccess_scraped import (
    ScrapedIncumbentElectionManager,
    ScrapedBallotMeasureManager,
    ScrapedRecallMeasureManager
)
from .opencivicdata import (
    OCDCandidacyQuerySet,
    OCDCandidacyManager,
    OCDCandidateContestQuerySet,
    OCDCandidateContestManager,
    OCDPartisanPrimaryManager,
    OCDElectionManager,
    OCDPartyManager,
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
    OCDSenatePostManager
)


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
    "OCDPartyManager",
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
    "OCDSenatePostManager"
)
