#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for OCD Filing related models..
"""
from __future__ import unicode_literals
from opencivicdata.campaign_finance.models import (
    Transaction,
    TransactionIdentifier
)
from calaccess_processed_elections.proxies import OCDProxyModelMixin
from postgres_copy import CopyManager
from calaccess_processed_campaignfinance.managers import OCDTransactionManager

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
        proxy = True


class OCDTransactionIdentifierProxy(TransactionIdentifier, OCDProxyModelMixin):
    """
    A proxy on the OCD TransactionIdentifier model.
    """
    objects = CopyManager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
