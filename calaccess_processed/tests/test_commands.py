#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for management commands.
"""
import os
import shutil
import calaccess_processed
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.models import Count
from django.utils.timezone import now
from datetime import date
from django.test import TestCase, override_settings
from calaccess_raw.models import RawDataVersion
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed import corrections
from calaccess_processed.models import ProcessedDataVersion, ScrapedCandidateProxy
from calaccess_scraped.models import Candidate as ScrapedCandidate
from calaccess_scraped.models import Proposition as ScrapedProposition
from opencivicdata.core.models import Person
from opencivicdata.elections.models import (
    BallotMeasureContest,
    Candidacy,
    CandidateContest,
    RetentionContest,
)


class NoProcessedDataTest(TestCase):
    """
    Tests to run with no data loaded.
    """
    def test_no_raw_data(self):
        """
        Confirm process command will not run without data.
        """
        with self.assertRaises(CommandError):
            call_command("processcalaccessdata", verbosity=3, noinput=True)


@override_settings(
    CALACCESS_DATA_DIR=os.path.join(settings.BASE_DIR, 'test-data')
)
@override_settings(
    MEDIA_ROOT=os.path.join(settings.BASE_DIR, 'test-data', ".media")
)
@override_settings(CALACCESS_STORE_ARCHIVE=True)
class ProcessedDataTest(TestCase):
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
    def setUpClass(cls):
        """
        Load data for other tests.
        """
        super(ProcessedDataTest, cls).setUpClass()
        # fake a raw data download
        download_dir = os.path.join(settings.CALACCESS_DATA_DIR, 'download')
        os.path.exists(download_dir) or os.mkdir(download_dir)
        zip_path = os.path.join(
            settings.CALACCESS_DATA_DIR,
            'dbwebexport.zip',
        )
        shutil.copy(zip_path, download_dir)
        RawDataVersion.objects.create(
            release_datetime=now(),
            download_start_datetime=now(),
            download_finish_datetime=now(),
            expected_size=os.stat(zip_path).st_size,
        )
        call_command("updatecalaccessrawdata", verbosity=3, noinput=True)
        call_command("processcalaccessdata", verbosity=3, noinput=True, scrape=False)

    def test_scraped_propositions(self):
        """
        Test the scraped propostions loaded into the database.
        """
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

    def test_scraped_candidates(self):
        """
        Test the scraped candidates loaded into the database.
        """
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

            # Confirm there aren't multiple Candidacies with the same candidate_name
            # unless party_id is different or person's filer_id is different
            candidate_name_groups_q = contest.candidacies.values(
                'candidate_name',
            ).annotate(
                row_count=Count('id'),
            ).order_by().filter(row_count__gt=1)

            # loop over each group of multiple candidacies sharing the same candidate_name
            for group in candidate_name_groups_q.all():
                candidacies_q = contest.candidacies.filter(
                    candidate_name=group['candidate_name'],
                )

                filer_id_party_groups_q = candidacies_q.filter(
                    person__identifiers__scheme='calaccess_filer_id'
                ).order_by(
                    'person__identifiers__identifier',
                    'party',
                ).values(
                    'person__identifiers__identifier',
                    'party',
                ).distinct()

                # confirm that count of candidacies equals count of
                # distinct filer_id/party groups
                self.assertEqual(
                    candidacies_q.count(),
                    filer_id_party_groups_q.count(),
                    msg='{0} candidacies in {1} with candidate_name "{2}" have {3} '
                        'distinct filer_id/party combos!'.format(
                        candidacies_q.count(),
                        contest,
                        group['candidate_name'],
                        filer_id_party_groups_q.count(),
                    ),
                )

            # Confirm there aren't multiple Candidacies with the same person.name
            # unless party_id is different or person's filer_id is different
            person_name_groups_q = contest.candidacies.values(
                'person__name',
            ).annotate(
                row_count=Count('id'),
            ).order_by().filter(row_count__gt=1)

            # loop over each group of multiple candidacies sharing the same candidate_name
            for group in person_name_groups_q.all():
                candidacies_q = contest.candidacies.filter(
                    person__name=group['person__name'],
                )

                filer_id_party_groups_q = candidacies_q.filter(
                    person__identifiers__scheme='calaccess_filer_id'
                ).order_by(
                    'person__identifiers__identifier',
                    'party',
                ).values(
                    'person__identifiers__identifier',
                    'party',
                ).distinct()

                # confirm that count of candidacies equals count of
                # distinct filer_id/party groups
                self.assertEqual(
                    candidacies_q.count(),
                    filer_id_party_groups_q.count(),
                    msg='{0} candidacies in {1} with person__name "{2}" have {3} '
                        'distinct filer_id/party combos!'.format(
                        candidacies_q.count(),
                        contest,
                        group['person__name'],
                        filer_id_party_groups_q.count(),
                    ),
                )

        # For each Person...
        for person in Person.objects.all():
            # Confirm name is same as most recent candidate_name
            latest_candidate_name = person.candidacies.latest(
                'contest__election__date'
            ).candidate_name

            self.assertEqual(
                person.name,
                latest_candidate_name,
                msg='Person.name "{0}" doesn\'t match latest candidate_name "{1}!'.format(
                    person.name,
                    latest_candidate_name,
                )
            )

    def test_processed_versions(self):
        """
        Test processed versions.
        """
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
        self.assertEqual(
            date(2016, 6, 7),
            calaccess_processed.get_expected_election_date(2016, 'PRIMARY'),
        )

    def test_2016_general_date(self):
        """
        Confirm correct calculation of 2016 general date.
        """
        self.assertEqual(
            date(2016, 11, 8),
            calaccess_processed.get_expected_election_date(2016, 'GENERAL'),
        )

    def test_2014_primary_date(self):
        """
        Confirm correct calculation of 2014 primary date.
        """
        self.assertEqual(
            date(2014, 6, 3),
            calaccess_processed.get_expected_election_date(2014, 'PRIMARY'),
        )

    def test_2010_general_date(self):
        """
        Confirm correct calculation of 2010 general date.
        """
        self.assertEqual(
            date(2010, 11, 2),
            calaccess_processed.get_expected_election_date(2010, 'GENERAL'),
        )

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
        self.assertEqual(correx.name, "REPUBLICAN")

    def test_correction_assignment_by_proxy(self):
        """
        Test that a correction is properly being applied when parties are retrieved.
        """
        obj = ScrapedCandidateProxy.objects.get(name='WINSTON, ALMA MARIE')
        self.assertEqual(obj.get_party().name, 'REPUBLICAN')
