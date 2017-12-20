#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PostgreSQL database customizations.
"""
from django.contrib.postgres.operations import CreateExtension


class CryptoExtension(CreateExtension):
    """
    Install the pgcrypto extension to PostgresSQL.
    """
    def __init__(self):
        """
        The name of the extension to install goes here.
        """
        self.name = 'pgcrypto'
