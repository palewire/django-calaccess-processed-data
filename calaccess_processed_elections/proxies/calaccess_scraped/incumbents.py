#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy model for augmenting ScrapedIncumbent model with methods useful for processing.
"""
from __future__ import unicode_literals
from .base import ScrapedNameMixin
from calaccess_scraped.models import Incumbent


class ScrapedIncumbentProxy(Incumbent, ScrapedNameMixin):
    """
    A proxy for the calaccess_scraped Incumbent model.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        app_label = "calaccess_processed_elections"
        proxy = True
        ordering = ['-session']
