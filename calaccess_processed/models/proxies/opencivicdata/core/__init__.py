#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from .divisions import OCDDivisionProxy
from .organizations import (
    OCDMembershipProxy,
    OCDOrganizationProxy,
    OCDOrganizationIdentifierProxy,
    OCDOrganizationNameProxy,
)
from .jurisdictions import OCDJurisdictionProxy
from .people import (
    OCDPersonProxy,
    OCDPersonIdentifierProxy,
    OCDPersonNameProxy,
)
from .posts import OCDPostProxy


__all__ = (
    "OCDDivisionProxy",
    "OCDMembershipProxy",
    "OCDOrganizationProxy",
    "OCDOrganizationIdentifierProxy",
    "OCDOrganizationNameProxy",
    "OCDJurisdictionProxy"
    "OCDPersonProxy",
    "OCDPersonIdentifierProxy",
    "OCDPersonNameProxy",
    "OCDPostProxy",
    "OCDJurisdictionProxy",
    "OCDPersonProxy"
)
