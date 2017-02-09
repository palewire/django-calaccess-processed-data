#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing candidate information scraped from the CAL-ACCESS website.
"""
from calaccess_processed.models.scraper.candidates.candidates import ScrapedCandidate
from calaccess_processed.models.scraper.candidates.elections import CandidateScrapedElection
from calaccess_processed.models.scraper.candidates.committees import ScrapedCandidateCommittee

__all__ = (
    'ScrapedCandidate',
    'CandidateScrapedElection',
    'ScrapedCandidateCommittee',
)
