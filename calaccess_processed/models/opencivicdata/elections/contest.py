#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OCD Election Contest-related models.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.scraped import (
    ScrapedCandidate,
    ScrapedProposition,
)
from calaccess_processed.models.opencivicdata.division import Division
from calaccess_processed.models.opencivicdata.base import (
    IdentifierBase,
    LinkBase,
    OCDIDField,
    OCDBase,
)
from calaccess_processed.models.opencivicdata.people_orgs import Membership


@python_2_unicode_compatible
class ContestBase(OCDBase):
    """
    A base class with properties shared by all contest types.
    """
    id = OCDIDField(
        ocd_type='contest',
        help_text='Open Civic Data-style id in the format ``ocd-contest/{{uuid}}``.',
    )
    name = models.CharField(
        max_length=300,
        help_text='Name of the contest, not necessarily as it appears on the '
                  'ballot.'
    )
    division = models.ForeignKey(
        'Division',
        related_name='divisions',
        help_text='Reference to the OCD ``Division`` that defines the '
                  'geographical scope of the contest, e.g., a specific '
                  'Congressional or State Senate district.',
    )
    election = models.ForeignKey(
        'Election',
        related_name='contests',
        help_text='Reference to the OCD ``Election`` in which the contest is '
                  'decided.',
    )

    def __str__(self):
        return self.id


@python_2_unicode_compatible
class ContestIdentifier(IdentifierBase):
    """
    Model for storing an OCD Contest's other identifiers.
    """
    contest = models.ForeignKey(
        ContestBase,
        related_name='identifiers'
    )

    def __str__(self):
        tmpl = '%s identifies %s'
        return tmpl % (self.identifier, self.contest)


@python_2_unicode_compatible
class ContestSource(LinkBase):
    """
    Model for storing sources for OCD ContestBase objects.
    """
    contest = models.ForeignKey(ContestBase, related_name='sources')

    def __str__(self):
        return self.url


class BallotMeasureContestManager(models.Manager):
    """
    Manager with custom methods for OCD ballot measure contest.
    """
    def load_raw_data(self):
        """
        Load BallotMeasureContest model from ScrapedProposition.
        """
        for p in ScrapedProposition.objects.all():
            # check if we already have a BallotMeasureContest for the prop
            q = ContestIdentifier.objects.filter(
                scheme='calaccess_measure_id',
                identifier=p.scraped_id,
            )
            if q.exists():
                contest = q[0]
                # if so, make sure the name is up-to-date
                if contest.name != p.name:
                    contest.name = p.name
                    contest.save()
            else:
                # Get the division: CA statewide
                division_obj = Division.objects.get(
                    id='ocd-division/country:us/state:ca'
                )
                # Get the election
                election_obj = p.election.get_or_create_election()[0]

                if 'RECALL' in p.name:
                    if p.name == '2003 RECALL QUESTION':
                        # look up most recently scraped record for Gov. Gray Davis
                        scraped_candidate = ScrapedCandidate.objects.filter(
                            name='DAVIS, GRAY',
                            office_name='GOVERNOR',
                        ).latest('created')
                    elif p.name == 'JUNE 3, 2008 - SPECIAL RECALL ELECTION - SENATE DISTRICT 12':
                        # look up most recently scraped record for Sen. Jeff Denham
                        scraped_candidate = ScrapedCandidate.objects.filter(
                            name='DENHAM, JEFF',
                            office_name='STATE SENATE 12',
                        ).latest('created')
                    else:
                        # TODO: integrate previous election results
                        # look up the person currently in the post
                        raise Exception(
                            "Missing Membership (Person and Post) for %s." % p.name
                        )

                    # get or create person and post objects
                    person = scraped_candidate.get_or_create_person()[0]
                    post = scraped_candidate.get_or_create_post()[0]
                    # get or create membership object
                    membership = Membership.objects.get_or_create(
                        person=person,
                        post=post,
                        organization=post.organization,
                    )[0]
                    # create the retention contest
                    contest = RetentionContest.objects.create(
                        election=election_obj,
                        division=division_obj,
                        name=p.name,
                        ballot_measure_type='initiative',
                        membership=membership,
                    )
                else:
                    if 'REFERENDUM' in p.name:
                        ballot_measure_type = 'referendum'
                    elif 'INITIATIVE' in p.name or 'INITATIVE' in p.name:
                        ballot_measure_type = 'initiative'
                    else:
                        ballot_measure_type = 'ballot measure'

                    contest = self.create(
                        election=election_obj,
                        division=division_obj,
                        name=p.name,
                        ballot_measure_type=ballot_measure_type,
                    )

                contest.identifiers.create(
                    scheme='calaccess_measure_id',
                    identifier=p.scraped_id,
                )

            if not contest.ballot_selections.filter(selection='Yes').exists():
                contest.ballot_selections.create(selection='Yes')
            if not contest.ballot_selections.filter(selection='No').exists():
                contest.ballot_selections.create(selection='No')

            contest.sources.update_or_create(
                url=p.url,
                note='Last scraped on {dt:%Y-%m-%d}'.format(
                    dt=p.last_modified,
                )
            )

        return


@python_2_unicode_compatible
class BallotMeasureContest(ContestBase):
    """
    Contest in which voters can affirm or reject a ballot measure.
    """
    objects = BallotMeasureContestManager()

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
        ('ballot-measure', 'Ballot Measure'),
        ('initiative', 'Initiative'),
        ('referendum', 'Referendum'),
        ('other', 'Other'),
    )
    ballot_measure_type = models.CharField(
        max_length=300,
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
    filing_deadline = models.DateField(
        null=True,
        help_text='Specifies the date and time when a candidate must have filed '
                  'for the contest for the office.',
    )
    runoff_for_contest = models.OneToOneField(
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
    number_elected = models.IntegerField(
        default=1,
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
    party = models.ForeignKey(
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
    membership = models.ForeignKey(
        'Membership',
        help_text='Reference to the OCD ``Membership`` that represents the '
                  'tenure of a particular person (i.e., OCD ``Person`` object) '
                  'in a particular public office (i.e., ``Post`` object).',
    )

    def __str__(self):
        return self.id
