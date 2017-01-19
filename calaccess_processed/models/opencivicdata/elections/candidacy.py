#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OCD Election Candidacy-related models.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.opencivicdata.base import (
    OCDIDField,
    OCDBase,
)


@python_2_unicode_compatible
class Candidacy(OCDBase):
    """
    Represents a person who is a candidate for a public office.

    If a candidate is running in multiple contests, each contest must have its
    own ``Candidate`` object. ``Candidate`` objects may not be reused between
    contests.
    """
    id = OCDIDField(
        ocd_type='candidacy',
        help_text='Open Civic Data-style id in the format ``ocd-candidacy/{{uuid}}``.',
    )
    ballot_name = models.CharField(
        max_length=300,
        help_text="The candidate's name as it will be displayed on the official ballot, "
                  'e.g. "Ken T. Cuccinelli II".',
    )
    person_id = models.ForeignKey(
        'Person',
        related_name='candidacies',
        null=True,
        help_text='Reference to an OCD ``Person`` who is the candidate.',
    )
    post_id = models.ForeignKey(
        'Post',
        related_name='candidates',
        null=True,
        help_text='References the ``Post`` that represents the public office '
                  'for which the candidate is competing.',
    )
    committee_id = models.ForeignKey(
        # this should be switched to Committee whenever we implement the
        # proposed campaign finance models
        'Organization',
        related_name='candidates',
        null=True,
        help_text='Reference to the OCD ``Committee`` that represents the '
                  "candidate's campaign finance committee for the contest."
    )
    filed_date = models.DateField(
        null=True,
        help_text='Specifies when the candidate filed for the contest.',
    )
    is_incumbent = models.NullBooleanField(
        null=True,
        help_text='Indicates whether the candidate is the incumbent for the '
                  'office associated with the contest.',
    )
    is_top_ticket = models.NullBooleanField(
        null=True,
        help_text='Indicates that the candidate is the top of a ticket that '
                  'includes multiple candidates. For example, the '
                  'candidate running for President is consider the top of the '
                  'President/Vice President ticket. In many states, this is '
                  'also true of the Governor/Lieutenant Governor.'
    )
    party_id = models.ForeignKey(
        'Party',
        related_name='candidates',
        null=True,
        help_text='Reference to and OCD ``Party`` with which the candidate is '
                  'affiliated.'
    )
    candidate_selection = models.ForeignKey(
        'CandidateSelection',
        related_name='candidacies',
        null=True,
        help_text='References the ``CandidateSelection`` for the candidate, '
                  'i.e., the option printed on the ballot the voter would '
                  'choose when voting for the candidate',
    )

    def __str__(self):
        return self.ballot_name
