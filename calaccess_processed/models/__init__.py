#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the models from submodules and thread them together.
"""
from calaccess_processed.models.campaign.entities import (
    Candidate,
    CandidateCommittee,
)
from calaccess_processed.models.campaign.filings.form460 import (
    Form460Filing,
    Form460FilingVersion,
    Form460ScheduleAItem,
    Form460ScheduleAItemVersion,
    Form460ScheduleCItem,
    Form460ScheduleCItemVersion,
    Form460ScheduleDItem,
    Form460ScheduleDItemVersion,
    Form460ScheduleEItem,
    Form460ScheduleEItemVersion,
    Form460ScheduleESubItem,
    Form460ScheduleESubItemVersion,
    Form460ScheduleFItem,
    Form460ScheduleFItemVersion,
    Form460ScheduleGItem,
    Form460ScheduleGItemVersion,
    Form460ScheduleIItem,
    Form460ScheduleIItemVersion,
)
from calaccess_processed.models.campaign.filings.schedule497 import (
    Schedule497Filing,
    Schedule497FilingVersion,
    Schedule497Part1Item,
    Schedule497Part1ItemVersion,
    Schedule497Part2Item,
    Schedule497Part2ItemVersion,
)
from calaccess_processed.models.scraped import (
    ScrapedElection,
    ScrapedCandidate,
    ScrapedCommittee,
    ScrapedProposition,
)
from calaccess_processed.models.common import (
    FilerIDValue,
    FilingIDValue,
)
from calaccess_processed.models.tracking import (
    ProcessedDataVersion,
    ProcessedDataFile,
)

__all__ = (
    'ProcessedDataVersion',
    'ProcessedDataFile',
    'Candidate',
    'CandidateCommittee',
<<<<<<< 5b29d4ab13134108b40b54de85afd96af400e3c8
    'Form460Filing',
    'Form460FilingVersion',
    'Form460ScheduleAItem',
    'Form460ScheduleAItemVersion',
    'Form460ScheduleCItem',
    'Form460ScheduleCItemVersion',
    'Form460ScheduleDItem',
    'Form460ScheduleDItemVersion',
    'Form460ScheduleEItem',
    'Form460ScheduleEItemVersion',
    'Form460ScheduleESubItem',
    'Form460ScheduleESubItemVersion',
    'Form460ScheduleFItem',
    'Form460ScheduleFItemVersion',
    'Form460ScheduleGItem',
    'Form460ScheduleGItemVersion',
    'Form460ScheduleIItem',
    'Form460ScheduleIItemVersion',
    'Schedule497Filing',
    'Schedule497FilingVersion',
    'Schedule497Part1Item',
    'Schedule497Part1ItemVersion',
    'Schedule497Part2Item',
    'Schedule497Part2ItemVersion',
=======
    'F460Filing',
    'F460FilingVersion',
>>>>>>> reworking candidates scraper
    'ScrapedElection',
    'ScrapedCandidate',
    'ScrapedCommittee',
    'ScrapedProposition',
    'FilerIDValue',
    'FilingIDValue',
)
