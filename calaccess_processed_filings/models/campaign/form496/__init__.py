#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Abstract base models for Form 496 models.
"""
from .filing import Form496Filing, Form496FilingVersion


__all__ = (
    "Form496Filing",
    "Form496FilingVersion",
)
