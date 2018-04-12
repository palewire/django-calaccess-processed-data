#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom managers for models from the calaccess_scraped app.
"""
from __future__ import unicode_literals
from calaccess_processed.managers import BulkLoadSQLManager


class ScrapedIncumbentElectionManager(BulkLoadSQLManager):
    """
    Manager with custom queryset and methods on the ScrapedIncumbentElectionProxy model.
    """
    def get_queryset(self):
        """
        Override the default manager to exclude blacklisted elections.
        """
        qs = super(ScrapedIncumbentElectionManager, self).get_queryset()
        # http://www.sos.ca.gov/elections/prior-elections/special-elections/
        blacklisted_elections = (
            '2017-10-2',
            '2015-11-30',
            '2015-9-28',
            '2014-9-29',
            '2014-3-17',
            '2001-3-6'
        )
        return qs.exclude(date__in=blacklisted_elections)


class ScrapedBallotMeasureManager(BulkLoadSQLManager):
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


class ScrapedRecallMeasureManager(BulkLoadSQLManager):
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
