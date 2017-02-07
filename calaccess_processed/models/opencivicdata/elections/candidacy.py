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
from calaccess_processed.models.opencivicdata.elections import ElectionIdentifier
from calaccess_processed.models.opencivicdata.elections.ballot_selection import CandidateSelection
from calaccess_processed.models.opencivicdata.elections.contest import CandidateContest
from calaccess_processed.models.scraped import ScrapedCandidate


class CandidacyManager(models.Manager):
    """
    Manager with custom methods for OCD Candidacy.
    """
    def load_raw_data(self):
        """
        Load Candidacy (and related models) from ScrapedCandidate.

        Models loaded (in order):
        1. Post
        2. CandidateContest
        3. CandidateSelection
        4. Person
        5. Candidacy
        """
        for sc in ScrapedCandidate.objects.all():
            # get or create the post
            post = sc.get_or_create_post()[0]

            # get the election
            elec = ElectionIdentifier.objects.get(
                scheme='calaccess_election_id',
                identifier=sc.election.scraped_id,
            ).election

            # get or create the CandidateContest (election and post)
            try:
                contest = CandidateContest.objects.filter(
                    election=elec,
                    division=post.division,
                    posts=post,
                )[0]
            except IndexError:
                contest = CandidateContest.objects.create(
                    election=elec,
                    division=post.division,
                    name=sc.office_name,
                )
                contest.posts.add(post)

                if 'SPECIAL' in sc.election.name:
                    contest.is_unexpired_term = True
                else:
                    contest.is_unexpired_term = False
                # TODO: set runoff_for_contest, party and number_elected
                contest.save()

            # get or create the Person
            person = sc.get_or_create_person()[0]

            # check to see if the person has any candidacies for the contest
            q = Candidacy.objects.filter(
                ballot_selection__contest=contest
            ).filter(person=person)
            if not q.exists():
                # create the CandidateSelection
                selection = CandidateSelection.objects.create(
                    contest=contest,
                )
                # TODO: set or update the endorsement_parties and is_write_in

                # create the Candidacy
                Candidacy.objects.create(
                    person=person,
                    ballot_name=sc.name,
                    post=post,
                    is_top_ticket=False,
                    ballot_selection=selection,
                    # TODO: set committee, is_incumbent and party
                )

        return


@python_2_unicode_compatible
class Candidacy(OCDBase):
    """
    Represents a person who is a candidate for a public office.

    If a candidate is running in multiple contests, each contest must have its
    own ``Candidate`` object. ``Candidate`` objects may not be reused between
    contests.
    """
    objects = CandidacyManager()

    id = OCDIDField(
        ocd_type='candidacy',
        help_text='Open Civic Data-style id in the format ``ocd-candidacy/{{uuid}}``.',
    )
    ballot_name = models.CharField(
        max_length=300,
        help_text="The candidate's name as it will be displayed on the official ballot, "
                  'e.g. "Ken T. Cuccinelli II".',
    )
    person = models.ForeignKey(
        'Person',
        related_name='candidacies',
        null=True,
        help_text='Reference to an OCD ``Person`` who is the candidate.',
    )
    post = models.ForeignKey(
        'Post',
        related_name='candidates',
        null=True,
        help_text='References the ``Post`` that represents the public office '
                  'for which the candidate is competing.',
    )
    committee = models.ForeignKey(
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
    party = models.ForeignKey(
        'Party',
        related_name='candidates',
        null=True,
        help_text='Reference to and OCD ``Party`` with which the candidate is '
                  'affiliated.'
    )
    ballot_selection = models.ForeignKey(
        'CandidateSelection',
        related_name='candidacies',
        null=True,
        help_text='References the ``CandidateSelection`` for the candidate, '
                  'i.e., the option printed on the ballot the voter would '
                  'choose when voting for the candidate',
    )

    def __str__(self):
        return self.ballot_name
