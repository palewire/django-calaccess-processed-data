#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the admins from submodules and thread them together.
"""
from calaccess_raw.admin.base import BaseAdmin
from calaccess_processed.admin.filings.campaign.form501 import (
    Form501FilingAdmin,
    Form501FilingVersionAdmin,
)
from calaccess_processed.admin.filings.campaign.form460 import (
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
    Form460ScheduleB2ItemOldAdmin,
    Form460ScheduleB2ItemVersionOldAdmin,
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
    Form460ScheduleHItemAdmin,
    Form460ScheduleHItemVersionAdmin,
    Form460ScheduleH2ItemOldAdmin,
    Form460ScheduleH2ItemVersionOldAdmin,
    Form460ScheduleIItemAdmin,
    Form460ScheduleIItemVersionAdmin,
)
from calaccess_processed.admin.filings.campaign.form497 import (
    Form497FilingAdmin,
    Form497FilingVersionAdmin,
    Form497Part1ItemAdmin,
    Form497Part1ItemVersionAdmin,
    Form497Part2ItemAdmin,
    Form497Part2ItemVersionAdmin,
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
    'Form501FilingAdmin',
    'Form501FilingVersionAdmin',
    'Form460FilingAdmin',
    'Form460FilingVersionAdmin',
    'Form460ScheduleAItemAdmin',
    'Form460ScheduleAItemVersionAdmin',
    'Form460ScheduleB1ItemAdmin',
    'Form460ScheduleB1ItemVersionAdmin',
    'Form460ScheduleB2ItemAdmin',
    'Form460ScheduleB2ItemVersionAdmin',
    'Form460ScheduleB2ItemOldAdmin',
    'Form460ScheduleB2ItemVersionOldAdmin',
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
    'Form460ScheduleHItemAdmin',
    'Form460ScheduleHItemVersionAdmin',
    'Form460ScheduleH2ItemOldAdmin',
    'Form460ScheduleH2ItemVersionOldAdmin',
    'Form460ScheduleIItemAdmin',
    'Form460ScheduleIItemVersionAdmin',
    'Form497FilingAdmin',
    'Form497FilingVersionAdmin',
    'Form497Part1ItemAdmin',
    'Form497Part1ItemVersionAdmin',
    'Form497Part2ItemAdmin',
    'Form497Part2ItemVersionAdmin',
    'FilerIDValueAdmin',
    'ProcessedDataVersionAdmin',
    'ProcessedDataFileAdmin',
)
