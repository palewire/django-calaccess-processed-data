#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for OCD's campaign finance models.
"""
from .committees import (
    OCDCommitteeProxy,
    OCDCommitteeIdentifierProxy,
    OCDCommitteeNameProxy,
    OCDCommitteeSourceProxy,
    OCDCommitteeTypeProxy
)
from .filings import (
    OCDFilingProxy,
    OCDFilingIdentifierProxy,
    OCDFilingSourceProxy,
    OCDFilingActionProxy,
    OCDFilingActionSummaryAmountProxy
)
from .transactions import (
    OCDTransactionProxy,
    OCDTransactionIdentifierProxy
)

__all__ = (
    'OCDCommitteeProxy',
    'OCDCommitteeIdentifierProxy',
    'OCDCommitteeNameProxy',
    'OCDCommitteeSourceProxy',
    'OCDCommitteeTypeProxy',
    'OCDFilingProxy',
    'OCDFilingIdentifierProxy',
    'OCDFilingSourceProxy',
    'OCDFilingActionProxy',
    'OCDFilingActionSummaryAmountProxy',
    'OCDTransactionProxy',
    'OCDTransactionIdentifierProxy',
)
