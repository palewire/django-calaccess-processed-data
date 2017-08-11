#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from .candidatecontests import OCDCandidateContestProxy
from .candidacies import OCDCandidacyProxy
from .divisions import OCDDivisionProxy
from .elections import OCDElectionProxy
from .organizations import (
    OCDMembershipProxy,
    OCDOrganizationProxy,
    OCDOrganizationIdentifierProxy,
    OCDOrganizationNameProxy,
)
from .parties import OCDPartyProxy
from .people import OCDPersonProxy, OCDPersonNameProxy
from .posts import OCDPostProxy


__all__ = (
    'OCDCandidateContestProxy',
    'OCDCandidacyProxy',
    'OCDDivisionProxy',
    'OCDElectionProxy',
    'OCDMembershipProxy',
    'OCDOrganizationProxy',
    'OCDOrganizationIdentifierProxy',
    'OCDOrganizationNameProxy',
    'OCDPartyProxy',
    'OCDPersonProxy',
    'OCDPersonNameProxy',
    'OCDPostProxy',
)
