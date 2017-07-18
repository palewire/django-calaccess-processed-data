#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from .candidates import ScrapedCandidateProxy
from .elections import ScrapedCandidateElectionProxy
from .parties import OCDPartyProxy

__all__ = (
    'ScrapedCandidateProxy',
    'ScrapedCandidateElectionProxy',
    'OCDPartyProxy'
)
