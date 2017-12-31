#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the managers from submodules and thread them together.
"""
from .campaign_finance import (
    BaseOCDBulkLoadSQLManager,
    OCDCommitteeManager,
    OCDCommitteeIdentifierManager,
    OCDCommitteeNameManager,
    OCDCommitteeTypeManager,
    OCDFilingManager,
    OCDFilingIdentifierManager,
    OCDFilingActionManager,
    OCDFilingActionSummaryAmountManager,
    OCDTransactionManager
)
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
    OCDSenatePostManager
)
from .elections import (
    OCDCandidacyQuerySet,
    OCDCandidacyManager,
    OCDCandidateContestQuerySet,
    OCDPartisanPrimaryManager,
    OCDElectionManager,
    OCDPartyManager
)


__all__ = (
    "BaseOCDBulkLoadSQLManager",
    "OCDCommitteeManager",
    "OCDCommitteeIdentifierManager",
    "OCDCommitteeNameManager",
    "OCDCommitteeTypeManager",
    "OCDFilingManager",
    "OCDFilingIdentifierManager",
    "OCDFilingActionManager",
    "OCDFilingActionSummaryAmountManager",
    "OCDTransactionManager",
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
    "OCDPartisanPrimaryManager",
    "OCDElectionManager",
    "OCDPartyManager"
)
