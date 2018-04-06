#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load the OCD Election model from the scraped PropositionElection model.
"""
from calaccess_processed.management.commands import LoadOCDElectionsBase
from calaccess_processed.models import ScrapedPropositionElectionProxy


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
