#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the managers from submodules and thread them together.
"""
from .flatfiles import (
    OCDFlatBallotMeasureContestManager,
    OCDFlatCandidacyManager,
    OCDFlatRetentionContestManager
)
from .proxies import (
    RawFilerToFilerTypeCdManager,
    ScrapedIncumbentElectionManager,
    ScrapedBallotMeasureManager,
    ScrapedRecallMeasureManager,
    BaseOCDBulkLoadSQLManager,
    OCDCommitteeManager,
    OCDCommitteeIdentifierManager,
    OCDCommitteeNameManager,
    OCDCommitteeTypeManager,
    OCDFilingManager,
    OCDFilingIdentifierManager,
    OCDFilingActionManager,
    OCDFilingActionSummaryAmountManager,
    OCDTransactionManager,
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
    OCDCandidacyQuerySet,
    OCDCandidacyManager,
    OCDCandidateContestQuerySet,
    OCDPartisanPrimaryManager,
    OCDElectionManager,
    OCDPartyManager
)
from .bulkloadsql import BulkLoadSQLManager
from .filings import (
    FilingsManager,
    Form501FilingManager
)


__all__ = (
    "OCDFlatBallotMeasureContestManager",
    "OCDFlatCandidacyManager",
    "OCDFlatRetentionContestManager",
    "RawFilerToFilerTypeCdManager",
    "ScrapedIncumbentElectionManager",
    "ScrapedBallotMeasureManager",
    "ScrapedRecallMeasureManager",
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
    "OCDPartyManager",
    'BulkLoadSQLManager',
    'FilingsManager',
    'Form501FilingManager'
)
