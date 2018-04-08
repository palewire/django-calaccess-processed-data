#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from .opencivicdata import (
    OCDProxyModelMixin,
    OCDDivisionProxy,
    OCDMembershipProxy,
    OCDJurisdictionProxy,
    OCDOrganizationProxy,
    OCDOrganizationIdentifierProxy,
    OCDOrganizationNameProxy,
    OCDPersonProxy,
    OCDPersonIdentifierProxy,
    OCDPersonNameProxy,
    OCDPostProxy
)
from .calaccess_raw import RawFilerToFilerTypeCdManager
from .calaccess_scraped import (
    ScrapedCandidateProxy,
    ScrapedIncumbentProxy,
    ScrapedCandidateElectionProxy,
    ScrapedIncumbentElectionProxy,
    ScrapedPropositionProxy,
    ScrapedPropositionElectionProxy
)


__all__ = (
    'RawFilerToFilerTypeCdManager',
    'ScrapedCandidateProxy',
    'ScrapedCandidateElectionProxy',
    'ScrapedIncumbentProxy',
    'ScrapedIncumbentElectionProxy',
    'ScrapedPropositionProxy',
    'ScrapedPropositionElectionProxy',
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
