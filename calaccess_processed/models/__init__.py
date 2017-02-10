#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the models from submodules and thread them together.
"""
from calaccess_processed.models.filings.campaign.entities import (
    Candidate,
    CandidateCommittee,
)
from calaccess_processed.models.filings.campaign.form460 import (
    Form460Filing,
    Form460FilingVersion,
)
from calaccess_processed.models.filings.campaign.form460.schedules.a import (
    Form460ScheduleAItem,
    Form460ScheduleAItemVersion,
)
from calaccess_processed.models.filings.campaign.form460.schedules.b import (
    Form460ScheduleB1Item,
    Form460ScheduleB1ItemVersion,
    Form460ScheduleB2Item,
    Form460ScheduleB2ItemVersion,
    Form460ScheduleB2ItemOld,
    Form460ScheduleB2ItemVersionOld,
)
from calaccess_processed.models.filings.campaign.form460.schedules.c import (
    Form460ScheduleCItem,
    Form460ScheduleCItemVersion,
)
from calaccess_processed.models.filings.campaign.form460.schedules.d import (
    Form460ScheduleDItem,
    Form460ScheduleDItemVersion,
)
from calaccess_processed.models.filings.campaign.form460.schedules.e import (
    Form460ScheduleEItem,
    Form460ScheduleEItemVersion,
    Form460ScheduleESubItem,
    Form460ScheduleESubItemVersion,
)
from calaccess_processed.models.filings.campaign.form460.schedules.f import (
    Form460ScheduleFItem,
    Form460ScheduleFItemVersion,
)
from calaccess_processed.models.filings.campaign.form460.schedules.g import (
    Form460ScheduleGItem,
    Form460ScheduleGItemVersion,
)
from calaccess_processed.models.filings.campaign.form460.schedules.h import (
    Form460ScheduleHItem,
    Form460ScheduleHItemVersion,
    Form460ScheduleH2ItemOld,
    Form460ScheduleH2ItemVersionOld,
)
from calaccess_processed.models.filings.campaign.form460.schedules.i import (
    Form460ScheduleIItem,
    Form460ScheduleIItemVersion,
)
from calaccess_processed.models.filings.campaign.schedule497 import (
    Schedule497Filing,
    Schedule497FilingVersion,
    Schedule497Part1Item,
    Schedule497Part1ItemVersion,
    Schedule497Part2Item,
    Schedule497Part2ItemVersion,
)
from calaccess_processed.models.scraper import (
    BaseScrapedModel,
    BaseScrapedElection,
    BaseScrapedCommittee,
    ScrapedProposition,
    PropositionScrapedElection,
    ScrapedPropositionCommittee,
    ScrapedCandidate,
    CandidateScrapedElection,
    ScrapedCandidateCommittee,
)
from calaccess_processed.models.research import (
    FilerIDValue,
    FilingIDValue,
)
from calaccess_processed.models.tracking import (
    ProcessedDataVersion,
    ProcessedDataFile,
)
from calaccess_processed.models.opencivicdata.division import Division
from calaccess_processed.models.opencivicdata.event import Event
from calaccess_processed.models.opencivicdata.elections import Election
from calaccess_processed.models.opencivicdata.elections.candidacy import Candidacy
from calaccess_processed.models.opencivicdata.elections.party import Party
from calaccess_processed.models.opencivicdata.elections.contest import (
    ContestBase,
    BallotMeasureContest,
    CandidateContest,
    RetentionContest,
)
from calaccess_processed.models.opencivicdata.elections.ballot_selection import (
    BallotSelectionBase,
    BallotMeasureSelection,
    CandidateSelection,
)
from calaccess_processed.models.opencivicdata.jurisdiction import (
    Jurisdiction,
    LegislativeSession
)
from calaccess_processed.models.opencivicdata.people_orgs import (
    Organization,
    OrganizationIdentifier,
    OrganizationName,
    OrganizationContactDetail,
    OrganizationLink,
    OrganizationSource,
    Person,
    PersonIdentifier,
    PersonName,
    PersonContactDetail,
    PersonLink,
    PersonSource,
    Post,
    PostContactDetail,
    PostLink,
    Membership,
    MembershipContactDetail,
    MembershipLink,
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
    'BaseScrapedModel',
    'BaseScrapedElection',
    'BaseScrapedCommittee',
    'ScrapedProposition',
    'PropositionScrapedElection',
    'ScrapedPropositionCommittee',
    'ScrapedCandidate',
    'CandidateScrapedElection',
    'ScrapedCandidateCommittee',
    'ProcessedDataVersion',
    'ProcessedDataFile',
    'Candidacy',
    'Division',
    'Event',
    'Election',
    'ContestBase',
    'BallotMeasureContest',
    'CandidateContest',
    'RetentionContest',
    'BallotSelectionBase',
    'BallotMeasureSelection',
    'CandidateSelection',
    'Jurisdiction',
    'LegislativeSession',
    'Organization',
    'OrganizationIdentifier',
    'OrganizationName',
    'OrganizationContactDetail',
    'OrganizationLink',
    'OrganizationSource',
    'Party',
    'Person',
    'PersonIdentifier',
    'PersonName',
    'PersonContactDetail',
    'PersonLink',
    'PersonSource',
    'Post',
    'PostContactDetail',
    'PostLink',
    'Membership',
    'MembershipContactDetail',
    'MembershipLink',
)
