#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for management commands.
"""
import os
import shutil
import calaccess_processed
from datetime import date
import time
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db.models import Count
from django.test import TestCase, override_settings
from django.utils.timezone import now
from email.utils import formatdate
from calaccess_raw.models import RawDataVersion
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.management.commands.verifycalaccessprocesseddata import Command as VerifyCmd # noqa
from calaccess_processed import corrections
from calaccess_processed.models import (
    ProcessedDataVersion,
    ScrapedCandidateProxy,
)
from calaccess_scraped.models import Candidate as ScrapedCandidate
from calaccess_scraped.models import Proposition as ScrapedProposition
from opencivicdata.core.models import Person
from opencivicdata.elections.models import (
    BallotMeasureContest,
    Candidacy,
    CandidateContest,
)
import requests_mock


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
    @requests_mock.Mocker()
    def setUpClass(cls, m):
        """
        Load data for other tests.
        """
        super(ProcessedDataTest, cls).setUpClass()
        # fake a previous raw data download
        download_dir = os.path.join(settings.CALACCESS_DATA_DIR, 'download')
        os.path.exists(download_dir) or os.mkdir(download_dir)
        zip_path = os.path.join(
            settings.CALACCESS_DATA_DIR,
            'dbwebexport.zip',
        )
        shutil.copy(zip_path, download_dir)
        rdv = RawDataVersion.objects.create(
            release_datetime=now(),
            update_start_datetime=now(),
            download_start_datetime=now(),
            download_finish_datetime=now(),
            expected_size=os.stat(zip_path).st_size,
        )
        # mock an SoS HEAD response
        imf_datetime = formatdate(
            time.mktime(rdv.release_datetime.timetuple()),
            usegmt=True,
        )
        headers = {
            'Content-Length': str(rdv.expected_size),
            'Accept-Ranges': 'bytes',
            'Last-Modified': imf_datetime,
            'Connection': 'keep-alive',
            'Date': imf_datetime,
            'Content-Type': 'application/zip',
            'ETag': '2320c8-30619331-c54f7dc0',
            'Server': 'Apache/2.2.3 (Red Hat)',
        }
        m.register_uri(
            'HEAD',
            'http://campaignfinance.cdn.sos.ca.gov/dbwebexport.zip',
            headers=headers,
        )

        call_command("updatecalaccessrawdata", verbosity=3, noinput=True)
        call_command("processcalaccessdata", verbosity=3, noinput=True)

    def runTest(self):
        """
        Added to allow calling test_ methods on instance of this class in py2.
        """
        pass

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

    def test_regular_assembly_contest_counts(self):
        """
        Confirm equality of actual and expected counts of assembly contests in each election.

        Test only prior elections.
        """
        passed, error_msg = VerifyCmd().test_regular_assembly_contest_counts()

        self.assertTrue(passed, error_msg)

    def test_regular_executive_contest_counts(self):
        """
        Confirm equality of actual and expected counts of senate contests in each election.

        Test only prior elections.
        """
        passed, error_msg = VerifyCmd().test_regular_executive_contest_counts()

        self.assertTrue(passed, error_msg)

    def test_regular_senate_contest_counts(self):
        """
        Confirm equality of actual and expected counts of senate contests in each election.

        Test only prior elections.
        """
        passed, error_msg = VerifyCmd().test_regular_senate_contest_counts()

        self.assertTrue(passed, error_msg)

    def test_regular_senate_contest_districts(self):
        """
        Confirm that no elections have senate contests in the wrong districts.
        """
        passed, error_msg = VerifyCmd().test_regular_senate_contest_districts()

        self.assertTrue(passed, error_msg)

    def test_for_duplicate_memberships(self):
        """
        Confirm there are no duplicate membership records.
        """
        passed, error_msg = VerifyCmd().test_for_duplicate_memberships()

        self.assertTrue(passed, error_msg)

    def test_scraped_candidates(self):
        """
        Test the scraped candidates loaded into the database.
        """
        # Confirm that the count of scraped candidates equals the count loaded
        # into Candidacy with a scraped source
        # minus one, since Jim Fitzgerald didn't really run in the
        # Dem primary in 2008
        self.assertEqual(
            ScrapedCandidate.objects.count() - 1,
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

    def test_processed_version_completed(self):
        """
        Test that the processed version was completed.
        """
        processed_version = ProcessedDataVersion.objects.latest('process_start_datetime')
        self.assertTrue(processed_version.update_completed)

    def test_flat_zip_archived(self):
        """
        Confirm that a flat zip was archived.
        """
        processed_version = ProcessedDataVersion.objects.latest('process_start_datetime')
        has_flat_zip = processed_version.zips.filter(
            zip_archive__icontains='flat'
        ).exists()
        self.assertTrue(has_flat_zip)

    def test_relational_zip_archived(self):
        """
        Confirm that a relational zip was archived.
        """
        processed_version = ProcessedDataVersion.objects.latest('process_start_datetime')
        has_relational_zip = processed_version.zips.filter(
            zip_archive__icontains='relational'
        ).exists()
        self.assertTrue(has_relational_zip)

    def test_zip_sizes(self):
        """
        Confirm that each archived zip's size is the same as the actual file size.
        """
        processed_version = ProcessedDataVersion.objects.latest('process_start_datetime')
        for z in processed_version.zips.all():
            self.assertEqual(
                z.zip_size,
                os.path.getsize(z.zip_archive.path)
            )

    def test_processed_file_finished(self):
        """
        Test that each processed file was marked finished.
        """
        processed_version = ProcessedDataVersion.objects.latest('process_start_datetime')

        for df in processed_version.files.all():
            self.assertTrue(df.process_finish_datetime)

    def test_processed_file_archived(self):
        """
        Test that each processed file was archived.
        """
        processed_version = ProcessedDataVersion.objects.latest('process_start_datetime')

        for df in processed_version.files.all():
            self.assertTrue(df.file_archive)

    def test_processed_file_size(self):
        """
        Test that each processed file_size is the same as file's size.
        """
        processed_version = ProcessedDataVersion.objects.latest('process_start_datetime')

        for df in processed_version.files.all():
            self.assertEqual(
                df.file_size,
                os.path.getsize(df.file_archive.path)
            )

    def test_processed_file_records_count(self):
        """
        Test that each processed records_count is the same as rows in file.
        """
        processed_version = ProcessedDataVersion.objects.latest('process_start_datetime')

        for df in processed_version.files.all():
            df.file_archive.open()
            row_count = sum(1 for _ in df.file_archive) - 1
            df.file_archive.close()

            self.assertEqual(
                df.records_count,
                row_count
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

    def test_flat_file_row_counts(self):
        """
        Test that count of rows in flat files is same as row count in base model.
        """
        processed_version = ProcessedDataVersion.objects.latest('process_start_datetime')

        flat_processed_files = [
            df for df in processed_version.files.all() if df.is_flat
        ]

        for df in flat_processed_files:
            # get count from archived file of flat model
            df.file_archive.open()
            flat_row_count = sum(1 for _ in df.file_archive) - 1
            df.file_archive.close()

            # get count from archived file of the base model
            base_model_name = df.model().base_model._meta.object_name
            base_model_df = processed_version.files.get(
                file_name=base_model_name
            )
            base_model_df.file_archive.open()
            base_row_count = sum(1 for _ in base_model_df.file_archive) - 1
            base_model_df.file_archive.close()

            self.assertEqual(
                flat_row_count,
                base_row_count,
            )
