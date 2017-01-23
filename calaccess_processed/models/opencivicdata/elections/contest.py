#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OCD Election Contest-related models.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.scraped import ScrapedProposition
from calaccess_processed.models.opencivicdata.elections import Election
from calaccess_processed.models.opencivicdata.division import Division
from calaccess_processed.models.opencivicdata.base import (
    OCDIDField,
    OCDBase,
)
import re
from datetime import datetime


class ContestBase(OCDBase):
    """
    An abstract base class with properties shared by all contest types.
    """
    name = models.CharField(
        max_length=300,
        help_text='Name of the contest, not necessarily as it appears on the '
                  'ballot.'
    )
    division_id = models.ForeignKey(
        'Division',
        related_name='%(class)s_contests',
        help_text='Reference to the OCD ``Division`` that defines the '
                  'geographical scope of the contest, e.g., a specific '
                  'Congressional or State Senate district.',
    )
    election_id = models.ForeignKey(
        'Election',
        related_name='%(class)s_contests',
        help_text='Reference to the OCD ``Election`` in which the contest is '
                  'decided.',
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


class BallotMeasureContestManager(models.Manager):
    """
    Manager with custom methods for OCD ballot measure contest.
    """

    def load_raw_data(self):
        """
        Load BallotMeasureContest model from ScrapedProposition.
        """

        self.all().delete()

        date_name_regex = r'^(?P<date>[A-Z]+\s\d{1,2},\s\d{4})\s(?P<name>.+)'
        
        for p in ScrapedProposition.objects.all():
            # Get the election
            match = re.match(date_name_regex, p.election.name)
            dt_obj = datetime.strptime(
                match.groupdict()['date'],
                '%B %d, %Y',
            )
            election_obj = Election.objects.get(
              start_time=dt_obj,
              name='{0} {1}'.format(
                    dt_obj.year,
                    match.groupdict()['name']
                )
            )

            # Get the division: CA statewide
            division_obj = Division.objects.get(
              id='ocd-division/country:us/state:ca'
            )

            # Measure is either an initiative or a referendum
            ballot_measure_type = ''
            if 'REFERENDUM' in p.name:
              ballot_measure_type = 'r'
            elif 'RECALL' in p.name:
              ballot_measure_type = 'o'
            else:
              ballot_measure_type = 'i'

            self.create(
                election_id=election_obj,
                division_id=division_obj,
                name=p.name,
                ballot_measure_type=ballot_measure_type
            )

        return


@python_2_unicode_compatible
class BallotMeasureContest(ContestBase):
    """
    Contest in which voters can affirm or reject a ballot measure.
    """

    objects = BallotMeasureContestManager()

    id = OCDIDField(
        ocd_type='ballotmeasurecontest',
        help_text='Open Civic Data-style id in the format ``ocd-'
                  'ballotmeasurecontest/{{uuid}}``.',
    )
    con_statement = models.TextField(
        blank=True,
        help_text='Specifies a statement in opposition to the ballot measure. '
                  'It does not necessarily appear on the ballot.',
    )
    effect_of_abstain = models.CharField(
        max_length=300,
        blank=True,
        help_text='Specifies the effect abstaining from voting on the ballot '
                  'measure, i.e., whether abstaining is considered a vote '
                  'against it.',
    )
    full_text = models.TextField(
        blank=True,
        help_text='Specifies the full text of the ballot measure as it appears '
                  'on the ballot.',
    )
    passage_threshold = models.CharField(
        max_length=300,
        blank=True,
        help_text='Specifies the threshold of votes the ballot measure needs '
                  'in order to pass (string). The default is a simple majority, '
                  'i.e., "50% plus one vote". Other common thresholds are "three-'
                  'fifths" and "two-thirds".',
    )
    pro_statement = models.TextField(
        blank=True,
        help_text='Specifies a statement in favor of the referendum. It does '
                  'not necessarily appear on the ballot.',
    )
    summary_text = models.TextField(
        blank=True,
        help_text='Specifies a short summary of the ballot measure that is on '
                  'the ballot, below the title, but above the text.',
    )
    BALLOT_MEASURE_TYPES = (
        ('b', 'ballot-measure'),
        ('i', 'initiative'),
        ('r', 'referendum'),
        ('o', 'other'),
    )
    ballot_measure_type = models.CharField(
        max_length=1,
        blank=True,
        choices=BALLOT_MEASURE_TYPES,
        help_text='Enumerated among:\n\t* ballot-measure: A catch-all for '
                  'generic types of non-candidate-based contests.\n\t* '
                  'initiative: These are usually citizen-driven measures to be '
                  'placed on the ballot. These could include both statutory '
                  'changes and constitutional amendments.\n\t* referendum: These '
                  'could include measures to repeal existing acts of legislation, '
                  'legislative referrals, and legislatively-referred state '
                  'constitutional amendments.\n\t* other: Anything that does not '
                  'fall into the above categories.'
    )
    other_type = models.CharField(
        max_length=300,
        blank=True,
        help_text='Allows for cataloging a new type of ballot measure option, '
                  'when type is specified as "other".',
    )

    def __str__(self):
        return self.id


@python_2_unicode_compatible
class CandidateContest(ContestBase):
    """
    Contest among candidates competing for election to a public office.
    """
    id = OCDIDField(
        ocd_type='candidatecontest',
        help_text='Open Civic Data-style id in the format ``ocd-'
                  'candidatecontest/{{uuid}}``.',
    )
    filing_deadline = models.DateField(
        null=True,
        help_text='Specifies the date and time when a candidate must have filed '
                  'for the contest for the office.',
    )
    runoff_for_contest_id = models.OneToOneField(
        'CandidateContest',
        related_name='runoff_contest',
        null=True,
        help_text='If this contest is a runoff to determine the outcome of a '
                  'previously undecided contest, reference to that '
                  '``CandidateContest``.',
    )
    is_unexpired_term = models.NullBooleanField(
        null=True,
        help_text='Indicates that the former public office holder vacated the '
                  'post before serving a full term.',
    )
    number_elected = models.CharField(
        max_length=300,
        blank=True,
        help_text='Number of candidates that are elected in the contest, i.e. '
                  "'N' of N-of-M.",
    )
    posts = models.ManyToManyField(
        'Post',
        help_text='References to the OCD ``Post`` representing the public '
                  'offices for which the candidates are competing. If multiple, '
                  'the primary post should be listed first, e.g., the id for the '
                  'President post should be listed before the id for Vice-'
                  'President.',
    )
    party_id = models.ForeignKey(
        'Party',
        null=True,
        help_text='If the contest is among candidates of the same political '
                  'party, e.g., a partisan primary election, reference to the '
                  'OCD ``Party`` representing that political party.',
    )

    def __str__(self):
        return self.id


@python_2_unicode_compatible
class RetentionContest(BallotMeasureContest):
    """
    Subclass of ``BallotMeasureContest`` wherein a person retains or loses an office.

    For example, a judicial retention or recall election.
    """
    membership_id = models.ForeignKey(
        'Membership',
        help_text='Reference to the OCD ``Membership`` that represents the '
                  'tenure of a particular person (i.e., OCD ``Person`` object) '
                  'in a particular public office (i.e., ``Post`` object).',
    )

    def __str__(self):
        return self.id
