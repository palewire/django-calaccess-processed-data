#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OCD Election BallotSelection-related models.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.opencivicdata.base import (
    OCDIDField,
    OCDBase,
)


@python_2_unicode_compatible
class BallotMeasureSelection(OCDBase):
    """
    A ballot option that a voter could select in a ballot measure contest.
    """
    id = OCDIDField(
        ocd_type='ballotmeasureselection',
        help_text='Open Civic Data-style id in the format ``ocd-'
                  'ballotmeasureselection/{{uuid}}``.',
    )
    contest = models.ForeignKey(
        'BallotMeasureContest',
        related_name='ballot_measure_selections',
        help_text='References the ``BallotMeasureContest`` in which the '
                  'selection is an option.',
    )
    selection = models.CharField(
        max_length=300,
        help_text='Selection text for the option on the ballot , e.g., "Yes", '
                  '"No", "Recall", "Don\'t recall".',
    )

    def __str__(self):
        return self.id


@python_2_unicode_compatible
class CandidateSelection(OCDBase):
    """
    A ballot option that a voter could select in a candidate contest.
    """
    id = OCDIDField(
        ocd_type='candidateselection',
        help_text='Open Civic Data-style id in the format ``ocd-'
                  'candidateselection/{{uuid}}``.',
    )
    contest = models.ForeignKey(
        'BallotMeasureContest',
        related_name='candidate_selections',
        help_text='References the ``CandidateContest`` in which the selection '
                  'is an option.',
    )
    endorsement_parties = models.ManyToManyField(
        'Party',
        help_text='Each ``Party`` that is endorsing the candidates associated '
                  'with the selection. The number of parties is unbounded in '
                  'cases where multiple parties endorse a single candidate/'
                  'ticket.',
    )
    is_write_in = models.NullBooleanField(
        null=True,
        help_text='Indicates that the particular ballot selection allows for '
                  'write-in candidates. If true, one or more write-in '
                  'candidates are allowed for this contest.',
    )

    def __str__(self):
        return self.id
