#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from .candidates import ScrapedCandidateProxy
from .candidateelections import ScrapedCandidateElectionProxy
from .incumbents import ScrapedIncumbentProxy
from .incumbentelections import ScrapedIncumbentElectionProxy
from .propositions import ScrapedPropositionProxy
from .propositionelections import ScrapedPropositionElectionProxy


__all__ = (
    'ScrapedCandidateProxy',
    'ScrapedCandidateElectionProxy',
    'ScrapedIncumbentProxy',
    'ScrapedIncumbentElectionProxy',
    'ScrapedPropositionProxy',
    'ScrapedPropositionElectionProxy',
)
