#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for management commands.
"""
import os
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.models import Count
from datetime import date
from django.test import TestCase, override_settings
from calaccess_raw import get_test_download_directory
from calaccess_processed.management.commands import (
    CalAccessCommand,
    LoadOCDModelsCommand,
)
from calaccess_processed.models import ProcessedDataVersion
from calaccess_scraped.models import Candidate as ScrapedCandidate
from calaccess_scraped.models import Proposition as ScrapedProposition
from opencivicdata.elections.models import (
    BallotMeasureContest,
    Candidacy,
    CandidateContest,
    RetentionContest,
)


@override_settings(CALACCESS_STORE_ARCHIVE=True)
class ProcessedDataCommandsTest(TestCase):
    """
    Run and test management commands.
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
        # into Candidacy with a scraped source
        self.assertEqual(
            ScrapedCandidate.objects.count(),
            Candidacy.objects.filter(
                sources__url__contains='http://cal-access.sos.ca.gov/Campaign/Candidates/list.aspx?view=certified' # noqa
            ).count(),
        )
        # For each CandidateContest...
        for contest in CandidateContest.objects.all():
            # Confirm there isn't more than one incumbent
            self.assertTrue(
                contest.candidacies.filter(is_incumbent=True).count() <= 1,
                msg="Multiple incumbents in {}!".format(contest),
            )

            # Confirm there aren't multiple Candidacies with the same person_id
            person_id_groups_q = contest.candidacies.values(
                'person_id',
            ).annotate(
                row_count=Count('id'),
            ).order_by().filter(row_count__gt=1)

            self.assertTrue(
                person_id_groups_q.count() == 0,
                msg="Multiple candidacies with same person_id in {}!".format(
                    contest
                ),
            )

            # Confirm there aren't multiple Candidacies with the same filer_id
            filer_id_groups_q = contest.candidacies.filter(
                person__identifiers__scheme='calaccess_filer_id'
            ).values(
                'person__identifiers__identifier'
            ).annotate(
                row_count=Count('id'),
            ).order_by().filter(row_count__gt=1)

            self.assertTrue(
                filer_id_groups_q.count() == 0,
                msg="Multiple candidacies with same filer_id in {}!".format(
                    contest
                ),
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
        for df in processed_version.files.all():
            # Confirm the update completed
            self.assertTrue(df.process_finish_datetime)
            # Confirm that csv files where archived
            self.assertTrue(df.file_archive)
            # Confirm the correct file size
            self.assertEqual(
                df.file_size,
                os.path.getsize(df.file_archive.path)
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
            date(2016, 6, 7),
            c.get_regular_election_date(2016, 'PRIMARY'),
        )

    def test_2016_general_date(self):
        """
        Confirm correct calculation of 2016 general date.
        """
        c = LoadOCDModelsCommand()
        self.assertEqual(
            date(2016, 11, 8),
            c.get_regular_election_date(2016, 'GENERAL'),
        )

    def test_2014_primary_date(self):
        """
        Confirm correct calculation of 2014 primary date.
        """
        c = LoadOCDModelsCommand()
        self.assertEqual(
            date(2014, 6, 3),
            c.get_regular_election_date(2014, 'PRIMARY'),
        )

    def test_2010_general_date(self):
        """
        Confirm correct calculation of 2010 general date.
        """
        c = LoadOCDModelsCommand()
        self.assertEqual(
            date(2010, 11, 2),
            c.get_regular_election_date(2010, 'GENERAL'),
        )
