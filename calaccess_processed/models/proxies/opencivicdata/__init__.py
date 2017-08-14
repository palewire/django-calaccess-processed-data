#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from .base import OCDProxyModelMixin
from .ballotmeasures import (
    OCDBallotMeasureContestProxy,
    OCDBallotMeasureContestIdentifierProxy,
    OCDBallotMeasureContestOptionProxy,
    OCDBallotMeasureContestSourceProxy,
)
from .candidatecontests import (
    OCDCandidateContestProxy,
    OCDCandidateContestPostProxy,
    OCDCandidateContestSourceProxy,
)
from .candidacies import OCDCandidacyProxy, OCDCandidacySourceProxy
from .divisions import OCDDivisionProxy
from .elections import (
    OCDElectionProxy,
    OCDElectionIdentifierProxy,
    OCDElectionSourceProxy,
)
from .organizations import (
    OCDMembershipProxy,
    OCDOrganizationProxy,
    OCDOrganizationIdentifierProxy,
    OCDOrganizationNameProxy,
)
from .parties import OCDPartyProxy
from .people import OCDPersonProxy, OCDPersonNameProxy
from .posts import OCDPostProxy
from .retentioncontests import (
    OCDRetentionContestProxy,
    OCDRetentionContestIdentifierProxy,
    OCDRetentionContestOptionProxy,
    OCDRetentionContestSourceProxy,
)


__all__ = (
    'OCDBallotMeasureContestProxy',
    'OCDBallotMeasureContestIdentifierProxy',
    'OCDBallotMeasureContestOptionProxy',
    'OCDBallotMeasureContestSourceProxy',
    'OCDCandidateContestProxy',
    'OCDCandidateContestPostProxy',
    'OCDCandidateContestSourceProxy',
    'OCDCandidacyProxy',
    'OCDCandidacySourceProxy',
    'OCDDivisionProxy',
    'OCDElectionProxy',
    'OCDElectionIdentifierProxy',
    'OCDElectionSourceProxy',
    'OCDMembershipProxy',
    'OCDOrganizationProxy',
    'OCDOrganizationIdentifierProxy',
    'OCDOrganizationNameProxy',
    'OCDPartyProxy',
    'OCDPersonProxy',
    'OCDPersonNameProxy',
    'OCDPostProxy',
    'OCDProxyModelMixin',
    'OCDRetentionContestProxy',
    'OCDRetentionContestIdentifierProxy',
    'OCDRetentionContestOptionProxy',
    'OCDRetentionContestSourceProxy',
)
