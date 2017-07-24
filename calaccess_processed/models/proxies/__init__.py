#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from .candidates import ScrapedCandidateProxy, ScrapedIncumbentProxy
from .candidacies import OCDCandidacyProxy
from .divisions import OCDDivisionProxy
from .elections import ScrapedCandidateElectionProxy
from .organizations import OCDOrganizationProxy
from .parties import OCDPartyProxy
from .people import OCDPersonProxy
from .posts import OCDPostProxy
from .candidatecontests import OCDRunoffProxy


__all__ = (
    'ScrapedCandidateProxy',
    'ScrapedCandidateElectionProxy',
    'ScrapedIncumbentProxy',
    'OCDCandidacyProxy',
    'OCDDivisionProxy',
    'OCDOrganizationProxy',
    'OCDPartyProxy',
    'OCDPersonProxy',
    'OCDPostProxy',
    'OCDRunoffProxy',
)
