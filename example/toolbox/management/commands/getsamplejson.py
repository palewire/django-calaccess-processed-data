#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Export sample json for OCDEP.
"""
from __future__ import print_function
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from calaccess_processed.models.opencivicdata.elections import Election
from calaccess_processed.models.opencivicdata.elections.ballot_selection import (
    BallotMeasureSelection,
    CandidateSelection,
)
from calaccess_processed.models.opencivicdata.elections.ballot_selection import (
    BallotSelectionBase,
    BallotMeasureSelection,
    CandidateSelection,
)
from calaccess_processed.models.opencivicdata.elections.candidacy import Candidacy
from calaccess_processed.models.opencivicdata.elections.contest import (
    ContestBase,
    BallotMeasureContest,
    CandidateContest,
    RetentionContest,
)
from calaccess_processed.models.opencivicdata.elections.party import Party
import re


class Command(BaseCommand):
    """
    Export sample json for OCDEP.
    """
    help = 'Export sample json for OCDEP.'

    def handle(self, *args, **options):
        """
        Do it.
        """
        self.encoder = DjangoJSONEncoder(indent=4)

        # Election
        elec = Election.objects.latest('start_time')
        full_elec = self.prep_dict(elec.__dict__).copy()
        full_elec.update(self.prep_dict(elec.event_ptr.__dict__))
        full_elec['identifiers'] = [
            self.prep_dict(i.__dict__) for i in elec.identifiers.all()
        ]

        print('Sample Election')
        print('+++++++++++++++\n\n')
        print('.. code:: javascript\n')
        print(self.encoder.encode(full_elec))
        print('--------------------------------------------------------')

        # ContestBase
        contest = ContestBase.objects.get(
            election=elec,
            name='STATE SENATE 01',
        )
        full_contest = self.prep_dict(contest.__dict__).copy()
        full_contest['identifiers'] = [
            self.prep_dict(i.__dict__) for i in contest.identifiers.all()
        ]

        print('Sample ContestBase')
        print('+++++++++++++++++++\n\n')
        print('.. code:: javascript\n')
        print(self.encoder.encode(full_contest))
        print('--------------------------------------------------------')

        # BallotMeasureContest
        ballot_measure = BallotMeasureContest.objects.get(
            election=elec,
            name='PROPOSITION 060- ADULT FILMS. CONDOMS. HEALTH REQUIREMENTS. INITIATIVE STATUTE.',
        )
        full_ballot_measure = self.prep_dict(ballot_measure.__dict__).copy()
        full_ballot_measure['identifiers'] = [
            self.prep_dict(i.__dict__) for i in ballot_measure.identifiers.all()
        ]

        print('Sample BallotMeasureContest')
        print('+++++++++++++++++++++++++++\n\n')
        print('.. code:: javascript\n')
        print(self.encoder.encode(full_ballot_measure))
        print('--------------------------------------------------------')

        # CandidateContest
        candidate_contest = CandidateContest.objects.get(
            election=elec,
            name='STATE SENATE 01',
        )
        full_candidate_contest = self.prep_dict(candidate_contest.__dict__).copy()
        full_candidate_contest['identifiers'] = [
            self.prep_dict(i.__dict__) for i in candidate_contest.identifiers.all()
        ]

        print('Sample CandidateContest')
        print('+++++++++++++++++++++++\n\n')
        print('.. code:: javascript\n')
        print(self.encoder.encode(full_candidate_contest))
        print('--------------------------------------------------------')
        
        # RetentionContest
        retention_contest = RetentionContest.objects.get(
            name='2003 RECALL QUESTION',
        )
        full_retention_contest = self.prep_dict(retention_contest.__dict__).copy()
        full_retention_contest['identifiers'] = [
            self.prep_dict(i.__dict__) for i in retention_contest.identifiers.all()
        ]

        print('Sample RetentionContest')
        print('+++++++++++++++++++++++\n\n')
        print('.. code:: javascript\n')
        print(self.encoder.encode(full_retention_contest))
        print('--------------------------------------------------------')

        # Candidacy
        candidacy = CandidateSelection.objects.filter(
            contest__election=elec,
            contest__name='STATE SENATE 01',
        )[0].candidacies.all()[0]
        full_candidacy = self.prep_dict(candidacy.__dict__).copy()

        print('Sample Candidacy')
        print('++++++++++++++++\n\n')
        print('.. code:: javascript\n')
        print(self.encoder.encode(full_candidacy))
        print('--------------------------------------------------------')
        
        # Party
        party = Party.objects.get(name='DEMOCRATIC')
        full_party = self.prep_dict(party.__dict__).copy()

        print('Sample Party')
        print('++++++++++++++++\n\n')
        print('.. code:: javascript\n')
        print(self.encoder.encode(full_party))
        print('--------------------------------------------------------')

        # BallotSelectionBase

        # BallotMeasureSelection

        # CandidateSelection
        candidate_selection = CandidateSelection.objects.filter(
            contest__election=elec,
            contest__name='STATE SENATE 01',
        )[0]
        print(dir(candidate_selection))
        full_candidate_selection = self.prep_dict(
            candidate_selection.__dict__
        ).copy()

        print('Sample CandidateSelection')
        print('++++++++++++++++++++++++++\n\n')
        print('.. code:: javascript\n')
        print(self.encoder.encode(full_candidate_selection))
        print('--------------------------------------------------------')

    def prep_dict(self, obj_dict):
        """
        Remove any keys from the object dict prefixed with '_'
        """
        cp_dict = obj_dict.copy() 
        for k in obj_dict:
            if re.match(r'^_.+$', k) or '_ptr_' in k:
                del cp_dict[k]

        if 'scheme' in cp_dict:
            _id = [k for k in cp_dict if k.endswith('_id')][0]
            del cp_dict[_id]
            del cp_dict['id']

        return cp_dict
