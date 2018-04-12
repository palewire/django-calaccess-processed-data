#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from .ballotmeasurecontests import (
    OCDBallotMeasureContestProxy,
    OCDBallotMeasureContestIdentifierProxy,
    OCDBallotMeasureContestOptionProxy,
    OCDBallotMeasureContestSourceProxy
)
from .candidatecontests import (
    OCDCandidateContestProxy,
    OCDCandidateContestPostProxy,
    OCDCandidateContestSourceProxy
)
from .candidacies import (
    OCDCandidacyProxy,
    OCDCandidacySourceProxy
)
from .elections import (
    OCDElectionProxy,
    OCDElectionIdentifierProxy,
    OCDElectionSourceProxy
)
from .parties import OCDPartyProxy
from .retentioncontests import (
    OCDRetentionContestProxy,
    OCDRetentionContestIdentifierProxy,
    OCDRetentionContestOptionProxy,
    OCDRetentionContestSourceProxy
)


__all__ = (
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
