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
from .elections import (
    OCDBallotMeasureContestProxy,
    OCDBallotMeasureContestIdentifierProxy,
    OCDBallotMeasureContestOptionProxy,
    OCDBallotMeasureContestSourceProxy,
    OCDCandidateContestProxy,
    OCDCandidateContestPostProxy,
    OCDCandidateContestSourceProxy,
    OCDCandidacyProxy,
    OCDCandidacySourceProxy,
    OCDElectionProxy,
    OCDElectionIdentifierProxy,
    OCDElectionSourceProxy,
    OCDPartyProxy,
    OCDRetentionContestProxy,
    OCDRetentionContestIdentifierProxy,
    OCDRetentionContestOptionProxy,
    OCDRetentionContestSourceProxy,
)

__all__ = (
    'RawFilerToFilerTypeCdManager',
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
    'OCDProxyModelMixin',
    "OCDBallotMeasureContestProxy",
    "OCDBallotMeasureContestIdentifierProxy",
    "OCDBallotMeasureContestOptionProxy",
    "OCDBallotMeasureContestSourceProxy",
    "OCDCandidateContestProxy",
    "OCDCandidateContestPostProxy",
    "OCDCandidateContestSourceProxy",
    "OCDCandidacyProxy",
    "OCDCandidacySourceProxy",
    "OCDElectionProxy",
    "OCDElectionIdentifierProxy",
    "OCDElectionSourceProxy",
    "OCDPartyProxy",
    "OCDRetentionContestProxy",
    "OCDRetentionContestIdentifierProxy",
    "OCDRetentionContestOptionProxy",
    "OCDRetentionContestSourceProxy"
)
