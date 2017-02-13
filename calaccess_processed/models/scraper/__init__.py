#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing information scraped from the CAL-ACCESS website.
"""
from calaccess_processed.models.scraper.base import (
    BaseScrapedModel,
    BaseScrapedElection,
    BaseScrapedCommittee
)
from calaccess_processed.models.scraper.candidates import (
    CandidateScrapedElection,
    ScrapedCandidate,
    ScrapedCandidateCommittee,
)
from calaccess_processed.models.scraper.propositions import (
    ScrapedProposition,
    PropositionScrapedElection,
    ScrapedPropositionCommittee,
)

__all__ = (
    'BaseScrapedModel',
    'BaseScrapedElection',
    'BaseScrapedCommittee',
    'CandidateScrapedElection',
    'ScrapedCandidate',
    'ScrapedCandidateCommittee',
    'ScrapedProposition',
    'PropositionScrapedElection',
    'ScrapedPropositionCommittee',
)
