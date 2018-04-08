#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from .base import OCDProxyModelMixin
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
