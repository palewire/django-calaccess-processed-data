#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for management commands.
"""
from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models import (
    ScrapedCandidate,
    ScrapedProposition,
)
from opencivicdata.models import (
    BallotMeasureContest,
    Candidacy,
    CandidateContest,
    RetentionContest,
)


class ProcessedDataCommandsTest(TestCase):
    """
    Run and test management commands.
    """
    fixtures = [
        'divisions.json',
        'candidate_scraped_elections.json',
        'scraped_candidates.json',
        'incumbent_scraped_elections.json',
        'scraped_incumbents.json',
        'proposition_scraped_elections.json',
        'scraped_propositions.json',
    ]

    def test_commands(self):
        """
        Run the data loading and processing commands.
        """
        with self.assertRaises(CommandError):
            call_command("processcalaccessdata", verbosity=3, noinput=True)
        call_command("updatecalaccessrawdata", verbosity=3, test_data=True, noinput=True)
        call_command("processcalaccessdata", verbosity=3, noinput=True)

        # Confirm count of scraped propositions with a name that doesn't
        # include "RECALL" equals the count of loaded BallotMeasureContest.
        self.assertEqual(
            ScrapedProposition.objects.exclude(
                name__icontains='RECALL'
            ).count(),
            BallotMeasureContest.objects.count(),
        )
        # Confirm count of scraped propositions with a name that includes "RECALL"
        # equals the count of loaded RetentionContest.
        self.assertEqual(
            ScrapedProposition.objects.filter(
                name__icontains='RECALL'
            ).count(),
            RetentionContest.objects.count(),
        )
        # Confirm that the count of scraped candidates equals the count loaded
        # into Candidacy
        self.assertEqual(
            ScrapedCandidate.objects.count(),
            Candidacy.objects.count(),
        )
        # Confirm that no CandidateContest has more than one incumbent
        for contest in CandidateContest.objects.all():
            self.assertTrue(
                contest.candidacies.filter(is_incumbent=True).count() <= 1,
                msg="Multiple incumbents in {}!".format(contest),
            )

    def test_base_command(self):
        """
        Test options on base commands.
        """
        c = CalAccessCommand()
        c.handle()
        c.header("")
        c.log("")
        c.success("")
        c.warn("")
        c.failure("")
        c.duration()
