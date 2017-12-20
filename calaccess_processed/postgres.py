#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PostgreSQL database customizations
"""
from django.contrib.postgres.operations import CreateExtension


class CryptoExtension(CreateExtension):

    def __init__(self):
        self.name = 'pgcrypto'
