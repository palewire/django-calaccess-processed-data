#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom managers for models from the calaccess_scraped app.
"""
from __future__ import unicode_literals
from django.db import models


class ScrapedIncumbentElectionManager(models.Manager):
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
