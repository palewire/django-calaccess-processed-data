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
from .bulkloadsql import BulkLoadSQLManager


__all__ = (
    "RawFilerToFilerTypeCdManager",
    "ScrapedIncumbentElectionManager",
    "ScrapedBallotMeasureManager",
    "ScrapedRecallMeasureManager",
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
    'BulkLoadSQLManager'
)
