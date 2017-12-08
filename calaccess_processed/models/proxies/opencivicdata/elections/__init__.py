#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from .ballotmeasurecontests import (
    OCDBallotMeasureContestProxy,
    OCDBallotMeasureContestIdentifierProxy,
    OCDBallotMeasureContestOptionProxy,
    OCDBallotMeasureContestSourceProxy,
    OCDFlatBallotMeasureContestProxy
)
from .candidatecontests import (
    OCDCandidateContestProxy,
    OCDCandidateContestPostProxy,
    OCDCandidateContestSourceProxy
)
from .candidacies import (
    OCDCandidacyProxy,
    OCDCandidacySourceProxy,
    OCDFlatCandidacyProxy
)
from .election import (
    OCDElectionProxy,
    OCDElectionIdentifierProxy,
    OCDElectionSourceProxy
)
from .parties import OCDPartyProxy
from .retentioncontests import (
    OCDRetentionContestProxy,
    OCDRetentionContestIdentifierProxy,
    OCDRetentionContestOptionProxy,
    OCDRetentionContestSourceProxy,
    OCDFlatRetentionContestProxy
)


__all__ = (
    "OCDBallotMeasureContestProxy",
    "OCDBallotMeasureContestIdentifierProxy",
    "OCDBallotMeasureContestOptionProxy",
    "OCDBallotMeasureContestSourceProxy",
    "OCDFlatBallotMeasureContestProxy",
    "OCDCandidateContestProxy",
    "OCDCandidateContestPostProxy",
    "OCDCandidateContestSourceProxy",
    "OCDCandidacyProxy",
    "OCDCandidacySourceProxy",
    "OCDFlatCandidacyProxy",
    "OCDElectionProxy",
    "OCDElectionIdentifierProxy",
    "OCDElectionSourceProxy",
    "OCDPartyProxy",
    "OCDRetentionContestProxy",
    "OCDRetentionContestIdentifierProxy",
    "OCDRetentionContestOptionProxy",
    "OCDRetentionContestSourceProxy",
    "OCDFlatRetentionContestProxy"
)
