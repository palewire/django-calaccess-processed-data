#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for OCD Filing related models..
"""
from __future__ import unicode_literals
import logging
from opencivicdata.campaign_finance.models import (
    Transaction,
    TransactionIdentifier
)
from postgres_copy import CopyManager
from ..base import OCDProxyModelMixin
from calaccess_processed.managers import OCDTransactionManager
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
