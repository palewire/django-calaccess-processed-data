#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for flat views of (not yet implemented) OCD campaign finance models.
"""
from django.db import models
from .base import OCDProxyModelMixin


class OCDFlatCommitteeProxy(models.Model, OCDProxyModelMixin):
    """
    Every campaign committee recorded in CAL-ACCESS.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
        verbose_name_plural = 'committees'


class OCDFlatContributionProxy(models.Model, OCDProxyModelMixin):
    """
    Every campaign contribution recorded in CAL-ACCESS.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
        verbose_name_plural = 'contributions'


class OCDFlatExpenditureProxy(models.Model, OCDProxyModelMixin):
    """
    Every campaign expenditure recorded in CAL-ACCESS.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
        verbose_name_plural = 'expenditures'
