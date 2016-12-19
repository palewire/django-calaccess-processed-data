#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the models from submodules and thread them together.
"""
from calaccess_processed.models.campaign.entities import (
    Candidate,
    CandidateCommittee,
)
from calaccess_processed.models.campaign.elections import (
    Election,
)
from calaccess_processed.models.campaign.propositions import (
    Proposition,
    PropositionCommittee,
)
from calaccess_processed.models.campaign.filings.form460 import (
    Form460Filing,
    Form460FilingVersion,
)
from calaccess_processed.models.campaign.filings.form460.schedules.a import (
    Form460ScheduleAItem,
    Form460ScheduleAItemVersion,
)
from calaccess_processed.models.campaign.filings.form460.schedules.b import (
    Form460ScheduleB1Item,
    Form460ScheduleB1ItemVersion,
    Form460ScheduleB2Item,
    Form460ScheduleB2ItemVersion,
    Form460ScheduleB2ItemOld,
    Form460ScheduleB2ItemVersionOld,
)
from calaccess_processed.models.campaign.filings.form460.schedules.c import (
    Form460ScheduleCItem,
    Form460ScheduleCItemVersion,
)
from calaccess_processed.models.campaign.filings.form460.schedules.d import (
    Form460ScheduleDItem,
    Form460ScheduleDItemVersion,
)
from calaccess_processed.models.campaign.filings.form460.schedules.e import (
    Form460ScheduleEItem,
    Form460ScheduleEItemVersion,
    Form460ScheduleESubItem,
    Form460ScheduleESubItemVersion,
)
from calaccess_processed.models.campaign.filings.form460.schedules.f import (
    Form460ScheduleFItem,
    Form460ScheduleFItemVersion,
)
from calaccess_processed.models.campaign.filings.form460.schedules.g import (
    Form460ScheduleGItem,
    Form460ScheduleGItemVersion,
)
from calaccess_processed.models.campaign.filings.form460.schedules.h import (
    Form460ScheduleHItem,
    Form460ScheduleHItemVersion,
    Form460ScheduleH2ItemOld,
    Form460ScheduleH2ItemVersionOld,
)
from calaccess_processed.models.campaign.filings.form460.schedules.i import (
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
    ScrapedProposition,
    PropositionScrapedElection,
    ScrapedPropositionCommittee,
    ScrapedCandidate,
    CandidateScrapedElection,
    ScrapedCandidateCommittee,
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
    'Candidate',
    'CandidateCommittee',
    'Form460Filing',
    'Form460FilingVersion',
    'Form460ScheduleAItem',
    'Form460ScheduleAItemVersion',
    'Form460ScheduleB1Item',
    'Form460ScheduleB1ItemVersion',
    'Form460ScheduleB2Item',
    'Form460ScheduleB2ItemVersion',
    'Form460ScheduleB2ItemOld',
    'Form460ScheduleB2ItemVersionOld',
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
    'Form460ScheduleHItem',
    'Form460ScheduleHItemVersion',
    'Form460ScheduleH2ItemOld',
    'Form460ScheduleH2ItemVersionOld',
    'Form460ScheduleIItem',
    'Form460ScheduleIItemVersion',
    'FilerIDValue',
    'FilingIDValue',
    'Schedule497Filing',
    'Schedule497FilingVersion',
    'Schedule497Part1Item',
    'Schedule497Part1ItemVersion',
    'Schedule497Part2Item',
    'Schedule497Part2ItemVersion',
    'ScrapedProposition',
    'PropositionScrapedElection',
    'ScrapedPropositionCommittee',
    'ScrapedCandidate',
    'CandidateScrapedElection',
    'ScrapedCandidateCommittee',
    'Election',
    'Proposition',
    'PropositionCommittee',
    'ProcessedDataVersion',
    'ProcessedDataFile',
)
