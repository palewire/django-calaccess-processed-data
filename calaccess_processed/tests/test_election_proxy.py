#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for management commands.
"""
from unittest import TestCase
from calaccess_processed.models import ScrapedCandidateElectionProxy


class ScrapedCandidatElectioneNameParsing(TestCase):
    """
    Test how candidate names are parsed from scraped data.
    """
    def test_parse_of_general_election_name(self):
        """
        Test .parse_election_name() on "2016 GENERAL".
        """
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
        parsed_name = ScrapedCandidateElectionProxy(name='2003 SPECIAL ELECTION (GOVERNOR)').parsed_name
        assert parsed_name == {
            'year': 2003,
            'type': 'SPECIAL ELECTION',
            'office': 'GOVERNOR',
            'district': None,
        }
