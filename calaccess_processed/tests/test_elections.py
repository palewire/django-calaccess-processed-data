#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for management commands.
"""
from datetime import date
from unittest import TestCase
from calaccess_processed_elections import get_expected_election_date


class ElectionDatesTest(TestCase):
    """
    Test election date parsing utilities.
    """
    def test_2016_primary_date(self):
        """
        Confirm correct calculation of 2016 primary date.
        """
        self.assertEqual(
            date(2016, 6, 7),
            get_expected_election_date(2016, 'PRIMARY'),
        )

    def test_2016_general_date(self):
        """
        Confirm correct calculation of 2016 general date.
        """
        self.assertEqual(
            date(2016, 11, 8),
            get_expected_election_date(2016, 'GENERAL'),
        )

    def test_2014_primary_date(self):
        """
        Confirm correct calculation of 2014 primary date.
        """
        self.assertEqual(
            date(2014, 6, 3),
            get_expected_election_date(2014, 'PRIMARY'),
        )

    def test_2010_general_date(self):
        """
        Confirm correct calculation of 2010 general date.
        """
        self.assertEqual(
            date(2010, 11, 2),
            get_expected_election_date(2010, 'GENERAL'),
        )


class CorrectionsTest(TestCase):
    """
    Test our corrections.
    """
    fixtures = [
        'divisions.json',
        'candidate_election.json',
        'candidate.json',
        'incumbent_election.json',
        'incumbent.json',
        'proposition_election.json',
        'proposition.json'
    ]

    def test_correction(self):
        """
        Test that we can retrieve a correction directly.
        """
        from calaccess_processed_elections import corrections
        correx = corrections.candidate_party(
            "WINSTON, ALMA MARIE",
            "2014",
            "PRIMARY",
            "GOVERNOR"
        )
        self.assertEqual(correx.name, "REPUBLICAN")

    def test_correction_assignment_by_proxy(self):
        """
        Test that a correction is properly being applied when parties are retrieved.
        """
        from calaccess_processed_elections.proxies import ScrapedCandidateProxy
        obj = ScrapedCandidateProxy.objects.get(name='WINSTON, ALMA MARIE')
        self.assertEqual(obj.get_party().name, 'REPUBLICAN')


class ScrapedCandidatElectioneNameParsingTest(TestCase):
    """
    Test how candidate names are parsed from scraped data.
    """
    def test_parse_of_general_election_name(self):
        """
        Test .parse_election_name() on "2016 GENERAL".
        """
        from calaccess_processed_elections.proxies import ScrapedCandidateElectionProxy
        parsed_name = ScrapedCandidateElectionProxy(name='2016 GENERAL').parsed_name
        assert parsed_name == {
            'year': 2016,
            'type': 'GENERAL',
            'office': None,
            'district': None,
        }

    def test_parse_of_state_senate_special_election_name(self):
        """
        Test .parse_election_name() on "2009 SPECIAL ELECTION (STATE SENATE 26)".
        """
        from calaccess_processed_elections.proxies import ScrapedCandidateElectionProxy
        parsed_name = ScrapedCandidateElectionProxy(name='2009 SPECIAL ELECTION (STATE SENATE 26)').parsed_name
        assert parsed_name == {
            'year': 2009,
            'type': 'SPECIAL ELECTION',
            'office': 'STATE SENATE',
            'district': 26,
        }

    def test_parse_of_assembly_special_runoff_name(self):
        """
        Test .parse_election_name() on "2010 SPECIAL RUNOFF (ASSEMBLY 72)".
        """
        from calaccess_processed_elections.proxies import ScrapedCandidateElectionProxy
        parsed_name = ScrapedCandidateElectionProxy(name='2010 SPECIAL RUNOFF (ASSEMBLY 72)').parsed_name
        assert parsed_name == {
            'year': 2010,
            'type': 'SPECIAL RUNOFF',
            'office': 'ASSEMBLY',
            'district': 72,
        }

    def test_parse_of_special_election_name_without_district(self):
        """
        Test .parse_election_name() on "2003 SPECIAL ELECTION (GOVERNOR)".
        """
        from calaccess_processed_elections.proxies import ScrapedCandidateElectionProxy
        parsed_name = ScrapedCandidateElectionProxy(name='2003 SPECIAL ELECTION (GOVERNOR)').parsed_name
        assert parsed_name == {
            'year': 2003,
            'type': 'SPECIAL ELECTION',
            'office': 'GOVERNOR',
            'district': None,
        }