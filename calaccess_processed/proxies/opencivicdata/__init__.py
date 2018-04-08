#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from .base import OCDProxyModelMixin
from .campaign_finance import (
    OCDCommitteeProxy,
    OCDCommitteeIdentifierProxy,
    OCDCommitteeNameProxy,
    OCDCommitteeSourceProxy,
    OCDCommitteeTypeProxy,
    OCDFilingProxy,
    OCDFilingIdentifierProxy,
    OCDFilingSourceProxy,
    OCDFilingActionProxy,
    OCDFilingActionSummaryAmountProxy,
    OCDTransactionProxy,
    OCDTransactionIdentifierProxy
)
from .core import (
    OCDDivisionProxy,
    OCDMembershipProxy,
    OCDOrganizationProxy,
    OCDOrganizationIdentifierProxy,
    OCDOrganizationNameProxy,
    OCDJurisdictionProxy,
    OCDPersonProxy,
    OCDPersonIdentifierProxy,
    OCDPersonNameProxy,
    OCDPostProxy
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
    'OCDDivisionProxy',
    'OCDFlatBallotMeasureContestProxy',
    'OCDFlatCandidacyProxy',
    'OCDFlatRetentionContestProxy',
    'OCDJurisdictionProxy',
    'OCDMembershipProxy',
    'OCDOrganizationProxy',
    'OCDOrganizationIdentifierProxy',
    'OCDOrganizationNameProxy',
    'OCDPersonProxy',
    'OCDPersonIdentifierProxy',
    'OCDPersonNameProxy',
    'OCDPostProxy',
    'OCDProxyModelMixin',
)
