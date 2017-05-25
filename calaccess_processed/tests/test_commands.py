#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for management commands.
"""
import os
from django.utils import timezone
from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from calaccess_raw import get_test_download_directory
from calaccess_processed.management.commands import (
    CalAccessCommand,
    LoadOCDModelsCommand,
)
from calaccess_processed.models import (
    ScrapedCandidate,
    ScrapedProposition,
    ProcessedDataVersion,
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

    @classmethod
    def setUp(self):
        """
        Set up test case.
        """
        test_tsv_dir = os.path.join(get_test_download_directory(), 'tsv')
        os.path.exists(test_tsv_dir) or os.makedirs(test_tsv_dir)

    def test_commands(self):
        """
        Run the data loading and processing commands.
        """
        with self.settings(CALACCESS_STORE_ARCHIVE=True):
            with self.assertRaises(CommandError):
                call_command("processcalaccessdata", verbosity=3, noinput=True)
            call_command("updatecalaccessrawdata", verbosity=3, test_data=True, noinput=True)
            call_command("processcalaccessdata", verbosity=3, noinput=True, scrape=False)

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
            Candidacy.objects.filter(
                sources__url__contains='http://cal-access.sos.ca.gov/Campaign/Candidates/list.aspx?view=certified' # noqa
            ).count(),
        )
        # Confirm that no CandidateContest has more than one incumbent
        for contest in CandidateContest.objects.all():
            self.assertTrue(
                contest.candidacies.filter(is_incumbent=True).count() <= 1,
                msg="Multiple incumbents in {}!".format(contest),
            )

        processed_version = ProcessedDataVersion.objects.latest('process_start_datetime')
        # Confirm that the version finished
        self.assertTrue(processed_version.update_completed)
        # Confirm that zip file was archived
        self.assertTrue(processed_version.zip_archive)
        # Confirm that the size is correct
        self.assertEqual(
            processed_version.zip_size,
            os.path.getsize(processed_version.zip_archive.path)
        )

        # For each processed data file...
        for df in processed_version.files:
            # Confirm the update completed
            self.assertTrue(df.update_completed)
            # Confirm that csv files where archived
            self.assertTrue(df.file_archive)
            # Confirm the correct file size
            self.assertEqual(
                df.file_size,
                os.path.getsize(processed_version.file_archive.path)
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

    def test_2016_primary_date(self):
        """
        Confirm correct calculation of 2016 primary date.
        """
        c = LoadOCDModelsCommand()
        self.assertEqual(
            timezone.datetime(
                2016, 6, 7, tzinfo=timezone.utc
            ),
            c.get_regular_election_date(2016, 'PRIMARY'),
        )

    def test_2016_general_date(self):
        """
        Confirm correct calculation of 2016 general date.
        """
        c = LoadOCDModelsCommand()
        self.assertEqual(
            timezone.datetime(
                2016, 11, 8, tzinfo=timezone.utc
            ),
            c.get_regular_election_date(2016, 'GENERAL'),
        )

    def test_2014_primary_date(self):
        """
        Confirm correct calculation of 2014 primary date.
        """
        c = LoadOCDModelsCommand()
        self.assertEqual(
            timezone.datetime(
                2014, 6, 3, tzinfo=timezone.utc
            ),
            c.get_regular_election_date(2014, 'PRIMARY'),
        )

    def test_2010_general_date(self):
        """
        Confirm correct calculation of 2010 general date.
        """
        c = LoadOCDModelsCommand()
        self.assertEqual(
            timezone.datetime(
                2010, 11, 2, tzinfo=timezone.utc
            ),
            c.get_regular_election_date(2010, 'GENERAL'),
        )
