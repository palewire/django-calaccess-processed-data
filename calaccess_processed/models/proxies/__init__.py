#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from .calaccess_raw import RawFilerToFilerTypeCdManager
from .calaccess_scraped import (
    ScrapedCandidateProxy,
    ScrapedIncumbentProxy,
    ScrapedCandidateElectionProxy,
    ScrapedIncumbentElectionProxy,
    ScrapedPropositionProxy,
    ScrapedPropositionElectionProxy
)
from .opencivicdata import (
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
    OCDTransactionIdentifierProxy,
    OCDDivisionProxy,
    OCDMembershipProxy,
    OCDJurisdictionProxy,
    OCDOrganizationProxy,
    OCDOrganizationIdentifierProxy,
    OCDOrganizationNameProxy,
    OCDPersonProxy,
    OCDPersonIdentifierProxy,
    OCDPersonNameProxy,
    OCDPostProxy,
    OCDProxyModelMixin
)


__all__ = (
    'RawFilerToFilerTypeCdManager',
    'ScrapedCandidateProxy',
    'ScrapedCandidateElectionProxy',
    'ScrapedIncumbentProxy',
    'ScrapedIncumbentElectionProxy',
    'ScrapedPropositionProxy',
    'ScrapedPropositionElectionProxy',
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
    'OCDJurisdictionProxy',
    'OCDMembershipProxy',
    'OCDOrganizationProxy',
    'OCDOrganizationIdentifierProxy',
    'OCDOrganizationNameProxy',
    'OCDPersonProxy',
    'OCDPersonIdentifierProxy',
    'OCDPersonNameProxy',
    'OCDPostProxy',
    'OCDProxyModelMixin'
)
