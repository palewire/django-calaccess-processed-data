#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the admins from submodules and thread them together.
"""
from calaccess_raw.admin.base import BaseAdmin
from calaccess_processed.admin.campaign.entities import (
    CandidateAdmin,
    CandidateCommitteeAdmin,
)
from calaccess_processed.admin.campaign.filings.form460 import (
    Form460FilingAdmin,
    Form460FilingVersionAdmin,
    Form460ScheduleAItemAdmin,
    Form460ScheduleAItemVersionAdmin,
    Form460ScheduleCItemAdmin,
    Form460ScheduleCItemVersionAdmin,
    Form460ScheduleB1ItemAdmin,
    Form460ScheduleB1ItemVersionAdmin,
    Form460ScheduleB2ItemAdmin,
    Form460ScheduleB2ItemVersionAdmin,
    Form460ScheduleDItemAdmin,
    Form460ScheduleDItemVersionAdmin,
    Form460ScheduleEItemAdmin,
    Form460ScheduleEItemVersionAdmin,
    Form460ScheduleESubItemAdmin,
    Form460ScheduleESubItemVersionAdmin,
    Form460ScheduleFItemAdmin,
    Form460ScheduleFItemVersionAdmin,
    Form460ScheduleGItemAdmin,
    Form460ScheduleGItemVersionAdmin,
    Form460ScheduleIItemAdmin,
    Form460ScheduleIItemVersionAdmin,
)
from calaccess_processed.admin.campaign.filings.schedule497 import (
    Schedule497FilingAdmin,
    Schedule497FilingVersionAdmin,
    Schedule497Part1ItemAdmin,
    Schedule497Part1ItemVersionAdmin,
    Schedule497Part2ItemAdmin,
    Schedule497Part2ItemVersionAdmin,
)
from calaccess_processed.admin.common import (
    FilerIDValueAdmin,
)
from calaccess_processed.admin.tracking import (
    ProcessedDataVersionAdmin,
    ProcessedDataFileAdmin,
)

__all__ = (
    'BaseAdmin',
    'CandidateAdmin',
    'CandidateCommitteeAdmin',
    'Form460FilingAdmin',
    'Form460FilingVersionAdmin',
    'Form460ScheduleAItemAdmin',
    'Form460ScheduleAItemVersionAdmin',
    'Form460ScheduleB1ItemAdmin',
    'Form460ScheduleB1ItemVersionAdmin',
    'Form460ScheduleB2ItemAdmin',
    'Form460ScheduleB2ItemVersionAdmin',
    'Form460ScheduleCItemAdmin',
    'Form460ScheduleCItemVersionAdmin',
    'Form460ScheduleDItemAdmin',
    'Form460ScheduleDItemVersionAdmin',
    'Form460ScheduleEItemAdmin',
    'Form460ScheduleEItemVersionAdmin',
    'Form460ScheduleESubItemAdmin',
    'Form460ScheduleESubItemVersionAdmin',
    'Form460ScheduleFItemAdmin',
    'Form460ScheduleFItemVersionAdmin',
    'Form460ScheduleGItemAdmin',
    'Form460ScheduleGItemVersionAdmin',
    'Form460ScheduleIItemAdmin',
    'Form460ScheduleIItemVersionAdmin',
    'Schedule497FilingAdmin',
    'Schedule497FilingVersionAdmin',
    'Schedule497Part1ItemAdmin',
    'Schedule497Part1ItemVersionAdmin',
    'Schedule497Part2ItemAdmin',
    'Schedule497Part2ItemVersionAdmin',
    'FilerIDValueAdmin',
    'ProcessedDataVersionAdmin',
    'ProcessedDataFileAdmin',
)
