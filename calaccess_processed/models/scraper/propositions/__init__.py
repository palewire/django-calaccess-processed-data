#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing proposition information scraped from the CAL-ACCESS website.
"""
from calaccess_processed.models.scraper.propositions.propositions import ScrapedProposition
from calaccess_processed.models.scraper.propositions.elections import PropositionScrapedElection
from calaccess_processed.models.scraper.propositions.committees import ScrapedPropositionCommittee


__all__ = (
    'ScrapedProposition',
    'PropositionScrapedElection',
    'ScrapedPropositionCommittee',
)
