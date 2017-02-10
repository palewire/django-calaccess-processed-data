#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the admins from submodules and thread them together.
"""
from .base import (
    DivisionAdmin,
    JurisdictionAdmin,
    LegislativeSessionAdmin,
    MembershipAdmin,
    OrganizationAdmin,
    PersonAdmin,
    PostAdmin
)
from .elections import (
    ElectionAdmin,
    PartyAdmin,
    BallotMeasureContestAdmin,
    BallotMeasureSelectionAdmin,
    CandidateContestAdmin,
    CandidateSelectionAdmin,
    RetentionContestAdmin,
    CandidacyAdmin
)

__all__ = (
    'DivisionAdmin',
    'JurisdictionAdmin',
    'LegislativeSessionAdmin',
    'MembershipAdmin',
    'OrganizationAdmin',
    'PersonAdmin',
    'PostAdmin',
    'ElectionAdmin',
    'PartyAdmin',
    'BallotMeasureContestAdmin',
    'BallotMeasureSelectionAdmin',
    'CandidateContestAdmin',
    'CandidateSelectionAdmin',
    'RetentionContestAdmin',
    'CandidacyAdmin'
)
