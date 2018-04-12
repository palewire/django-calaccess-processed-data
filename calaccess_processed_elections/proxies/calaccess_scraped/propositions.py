#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy model for augmenting ScrapedProposition model with methods useful for processing.
"""
from __future__ import unicode_literals
from calaccess_scraped.models import Proposition
from .propositionelections import ScrapedPropositionElectionProxy
from calaccess_processed_elections.managers import (
    ScrapedBallotMeasureManager,
    ScrapedRecallMeasureManager
)


class ScrapedPropositionProxy(Proposition):
    """
    A proxy for the Proposition model in calaccess_scraped.
    """
    ballot_measures = ScrapedBallotMeasureManager()
    recall_measures = ScrapedRecallMeasureManager()

    class Meta:
        """
        Make this a proxy model.
        """
        app_label = "calaccess_processed_elections"
        proxy = True

    @property
    def election_proxy(self):
        """
        Return the proxy model for the related election object.
        """
        return ScrapedPropositionElectionProxy.objects.get(id=self.election.id)

    @property
    def classification(self):
        """
        Clean up the type of proposition this is for standardizing in OCD models.
        """
        # Set the classification
        if 'REFERENDUM' in self.name:
            return 'referendum'
        elif ('INITIATIVE' in self.name or 'INITATIVE' in self.name):
            return 'initiative'
        else:
            return 'ballot measure'
