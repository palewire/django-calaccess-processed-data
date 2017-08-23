#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from .base import OCDProxyModelMixin
from .ballotmeasurecontests import (
    OCDBallotMeasureContestProxy,
    OCDBallotMeasureContestIdentifierProxy,
    OCDBallotMeasureContestOptionProxy,
    OCDBallotMeasureContestSourceProxy,
    OCDFlatBallotMeasureContestProxy,
)
from .candidatecontests import (
    OCDCandidateContestProxy,
    OCDCandidateContestPostProxy,
    OCDCandidateContestSourceProxy,
)
from .candidacies import (
    OCDCandidacyProxy,
    OCDCandidacySourceProxy,
    OCDFlatCandidacyProxy,
)
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
from .people import (
    OCDPersonProxy,
    OCDPersonIdentifierProxy,
    OCDPersonNameProxy,
)
from .posts import OCDPostProxy
from .retentioncontests import (
    OCDRetentionContestProxy,
    OCDRetentionContestIdentifierProxy,
    OCDRetentionContestOptionProxy,
    OCDRetentionContestSourceProxy,
    OCDFlatRetentionContestProxy,
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
    'OCDFlatBallotMeasureContestProxy',
    'OCDFlatCandidacyProxy',
    'OCDFlatRetentionContestProxy',
    'OCDMembershipProxy',
    'OCDOrganizationProxy',
    'OCDOrganizationIdentifierProxy',
    'OCDOrganizationNameProxy',
    'OCDPartyProxy',
    'OCDPersonProxy',
    'OCDPersonIdentifierProxy',
    'OCDPersonNameProxy',
    'OCDPostProxy',
    'OCDProxyModelMixin',
    'OCDRetentionContestProxy',
    'OCDRetentionContestIdentifierProxy',
    'OCDRetentionContestOptionProxy',
    'OCDRetentionContestSourceProxy',
)
