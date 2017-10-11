#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy model for augmenting ScrapedProposition model with methods useful for processing.
"""
from __future__ import unicode_literals
from calaccess_scraped.models import Proposition
from django.db import models
from .propositionelections import ScrapedPropositionElectionProxy


class ScrapedBallotMeasureManager(models.Manager):
    """
    Custom manager that filters ScrapedProposition model to ballot measures.
    """
    def get_queryset(self):
        """
        Filter to ballot measures.
        """
        return super(
            ScrapedBallotMeasureManager, self
        ).get_queryset().exclude(name__icontains='RECALL')


class ScrapedRecallMeasureManager(models.Manager):
    """
    Custom manager that filters ScrapedProposition model to recall measures.
    """
    def get_queryset(self):
        """
        Filter to recall measures.
        """
        return super(
            ScrapedRecallMeasureManager, self
        ).get_queryset().filter(name__icontains='RECALL')


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
