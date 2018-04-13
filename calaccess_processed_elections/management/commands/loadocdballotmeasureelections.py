#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load the OCD Election model from the scraped PropositionElection model.
"""
from __future__ import unicode_literals
from calaccess_processed_elections.proxies import ScrapedPropositionElectionProxy
from calaccess_processed_elections.management.commands import LoadOCDElectionsBase


class Command(LoadOCDElectionsBase):
    """
    Load the OCD Election model from the scraped PropositionElection model.
    """
    help = 'Load the OCD Election model from the scraped PropositionElection model'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.header("Loading Elections from scraped propositions")
        self.load_from_proxy(ScrapedPropositionElectionProxy)
        self.success("Done!")
