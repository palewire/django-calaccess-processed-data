#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from .candidates import ScrapedCandidateProxy
from .divisions import OCDDivisionProxy
from .elections import ScrapedCandidateElectionProxy
from .organizations import OCDOrganizationProxy
from .parties import OCDPartyProxy
from .posts import OCDPostProxy


__all__ = (
    'ScrapedCandidateProxy',
    'ScrapedCandidateElectionProxy',
    'OCDDivisionProxy',
    'OCDOrganizationProxy',
    'OCDPartyProxy',
    'OCDPostProxy',
)
