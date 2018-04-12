#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for OCD Filing related models..
"""
from __future__ import unicode_literals

# Models
from calaccess_processed.proxies import OCDProxyModelMixin
from opencivicdata.campaign_finance.models import Transaction, TransactionIdentifier

# Managers
from calaccess_processed_campaignfinance.managers import OCDTransactionManager, CampaignFinanceManager

# Logging
import logging
logger = logging.getLogger(__name__)


class OCDTransactionProxy(Transaction, OCDProxyModelMixin):
    """
    A proxy on the OCD Transaction model.
    """
    objects = OCDTransactionManager()

    class Meta:
        """
        Make this a proxy model.
        """
        app_label = "calaccess_processed_campaignfinance"
        proxy = True


class OCDTransactionIdentifierProxy(TransactionIdentifier, OCDProxyModelMixin):
    """
    A proxy on the OCD TransactionIdentifier model.
    """
    objects = CampaignFinanceManager()

    class Meta:
        """
        Make this a proxy model.
        """
        app_label = "calaccess_processed_campaignfinance"
        proxy = True
