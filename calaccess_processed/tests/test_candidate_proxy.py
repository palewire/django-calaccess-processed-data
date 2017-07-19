#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for election proxy.
"""
from django.test import TestCase
from calaccess_processed import corrections
from calaccess_processed.models import ScrapedCandidateProxy


class ScrapedCandidatePartyAssignment(TestCase):
    """
    Test how scraped candidates are assigned a party.
    """
    fixtures = [
        'divisions.json',
        'candidate_election.json',
        'candidate.json',
        'incumbent_election.json',
        'incumbent.json',
        'proposition_election.json',
        'proposition.json',
    ]

    def test_correction(self):
        """
        Test that we can retrieve a correction directly.
        """
        correx = corrections.candidate_party(
            "WINSTON, ALMA MARIE",
            "2014",
            "PRIMARY",
            "GOVERNOR"
        )
        self.assertEqual(correx, "REPUBLICAN")

    def test_correction_assignment_by_proxy(self):
        """
        Test that a correction is properly being applied when parties are retrieved.
        """
        obj = ScrapedCandidateProxy.objects.get(name='WINSTON, ALMA MARIE')
        self.assertEqual(obj.get_party(), 'REPUBLICAN')
