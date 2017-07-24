#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from .candidacies import OCDCandidacyProxy
from .divisions import OCDDivisionProxy
from .elections import OCDElectionProxy
from .organizations import OCDOrganizationProxy
from .parties import OCDPartyProxy
from .people import OCDPersonProxy
from .posts import OCDPostProxy
from .candidatecontests import OCDRunoffProxy


__all__ = (
    'OCDCandidacyProxy',
    'OCDDivisionProxy',
    'OCDElectionProxy',
    'OCDOrganizationProxy',
    'OCDPartyProxy',
    'OCDPersonProxy',
    'OCDPostProxy',
    'OCDRunoffProxy',
)
