#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the managers from submodules and thread them together.
"""
from .calaccess_raw import RawFilerToFilerTypeCdManager
from .calaccess_scraped import ScrapedIncumbentElectionManager
from .opencivicdata import (
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
from .constraints import ConstraintsManager
from .filings import FilingsManager


__all__ = (
    "RawFilerToFilerTypeCdManager",
    "ScrapedIncumbentElectionManager",
    "OCDCommitteeManager",
    "OCDCommitteeIdentifierManager",
    "OCDCommitteeNameManager",
    "OCDCommitteeTypeManager",
    "OCDFilingManager",
    "OCDFilingIdentifierManager",
    "OCDFilingActionManager",
    "OCDFilingActionSummaryAmountManager",
    "OCDTransactionManager",
    'ConstraintsManager',
    'FilingsManager'
)
