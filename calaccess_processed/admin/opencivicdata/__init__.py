#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the admins from submodules and thread them together.
"""
from .base import (
    DivisionAdmin,
    OrganizationAdmin
)
from .elections import (
    ElectionAdmin,
    PartyAdmin
)

__all__ = (
    'DivisionAdmin',
    'OrganizationAdmin',
    'ElectionAdmin',
    'PartyAdmin'
)
