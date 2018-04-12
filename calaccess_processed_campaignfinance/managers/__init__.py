#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the managers from submodules and thread them together.
"""
from .base import CampaignFinanceManager
from .committees import (
    OCDCommitteeManager,
    OCDCommitteeIdentifierManager,
    OCDCommitteeNameManager,
    OCDCommitteeTypeManager
)
from .filings import (
    OCDFilingManager,
    OCDFilingIdentifierManager,
    OCDFilingActionManager,
    OCDFilingActionSummaryAmountManager
)
from .transactions import OCDTransactionManager


__all__ = (
    "CampaignFinanceManager",
    "OCDCommitteeManager",
    "OCDCommitteeIdentifierManager",
    "OCDCommitteeNameManager",
    "OCDCommitteeTypeManager",
    "OCDFilingManager",
    "OCDFilingIdentifierManager",
    "OCDFilingActionManager",
    "OCDFilingActionSummaryAmountManager",
    "OCDTransactionManager"
)
