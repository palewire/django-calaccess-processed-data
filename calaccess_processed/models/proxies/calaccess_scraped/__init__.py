#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from .candidates import ScrapedCandidateProxy, ScrapedIncumbentProxy
from .elections import ScrapedCandidateElectionProxy


__all__ = (
    'ScrapedCandidateProxy',
    'ScrapedCandidateElectionProxy',
    'ScrapedIncumbentProxy',
)
