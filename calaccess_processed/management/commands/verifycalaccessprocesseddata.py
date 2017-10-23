#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Check for mistakes in processed data loaded from CAL-ACCESS.
"""
from django.utils.timezone import now
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models import OCDElectionProxy, OCDMembershipProxy


class Command(CalAccessCommand):
    """
    Check for mistakes in processed data loaded from CAL-ACCESS.
    """
    help = 'Check for mistakes in processed data loaded from CAL-ACCESS.'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        exec_ok, exec_msg = self.test_regular_executive_contest_counts()
        if exec_ok:
            self.success('  State Executive office contests verified.')
        else:
            self.failure(exec_msg)

        sen_ok, sen_msg = self.test_regular_senate_contest_counts()
        if sen_ok:
            self.success('  State Senate contests verified.')
        else:
            self.failure(sen_msg)

        sen_dists_ok, sen_dists_msg = self.test_regular_senate_contest_districts()
        if sen_dists_ok:
            self.success('  State Senate districts verified.')
        else:
            self.failure(sen_dists_msg)

        asm_ok, asm_msg = self.test_regular_assembly_contest_counts()
        if asm_ok:
            self.success('  State Assembly contests verified.')
        else:
            self.failure(asm_msg)

        mems_ok, mems_msg = self.test_for_duplicate_memberships()
        if mems_ok:
            self.success('  No duplicate office holders')
        else:
            self.failure(mems_msg)

    def test_regular_assembly_contest_counts(self):
        """
        Confirm equality of actual and expected counts of assembly contests in each election.

        Test only prior elections.

        Return a tuple with boolean value (True means passed) and error message.
        """
        bad_elections = [
            e for e in OCDElectionProxy.objects.filter(date__year__lte=now().year)
            if e.regular_assembly_contest_count_actual != e.regular_assembly_contest_count_expected
        ]
        error_count = len(bad_elections)
        error_list = '\n'.join([
            '- {0} should have {1}, but has {2}'.format(
                e, e.regular_assembly_contest_count_expected, e.regular_assembly_contest_count_actual
            ) for e in bad_elections]
        )
        msg = 'Actual and expected counts of assembly contests not equal in {0} \
elections:\n{1}'.format(error_count, error_list)

        return (error_count == 0, msg)

    def test_regular_executive_contest_counts(self):
        """
        Confirm equality of actual and expected counts of senate contests in each election.

        Test only prior elections.

        Return a tuple with boolean value (True means passed) and error message.
        """
        bad_elections = [
            e for e in OCDElectionProxy.objects.filter(date__year__lte=now().year)
            if e.regular_executive_contest_count_actual != e.regular_executive_contest_count_expected
        ]
        error_count = len(bad_elections)
        error_list = '\n'.join([
            '- {0} should have {1}, but has {2}'.format(
                e, e.regular_executive_contest_count_expected, e.regular_executive_contest_count_actual
            ) for e in bad_elections]
        )
        msg = 'Actual and expected counts of executive contests not equal in {0} \
elections:\n{1}'.format(error_count, error_list)

        return (error_count == 0, msg)

    def test_regular_senate_contest_counts(self):
        """
        Confirm equality of actual and expected counts of senate contests in each election.

        Test only prior elections.

        Return a tuple with boolean value (True means passed) and error message.
        """
        bad_elections = [
            e for e in OCDElectionProxy.objects.filter(date__year__lte=now().year)
            if e.regular_senate_contest_count_actual != e.regular_senate_contest_count_expected
        ]
        error_count = len(bad_elections)
        error_list = '\n'.join([
            '- {0} should have {1}, but has {2}'.format(
                e, e.regular_senate_contest_count_expected, e.regular_senate_contest_count_actual
            ) for e in bad_elections]
        )
        msg = 'Actual and expected counts of senate contests not equal in {0} \
elections:\n{1}'.format(error_count, error_list)

        return (error_count == 0, msg)

    def test_regular_senate_contest_districts(self):
        """
        Confirm that no elections have senate contests in the wrong districts.

        Return a tuple with boolean value (True means passed) and error message.
        """
        bad_elections = {}
        for e in OCDElectionProxy.objects.all():
            bad_senate_contests = e.get_regular_senate_contests_in_wrong_districts()
            if len(bad_senate_contests) > 0:
                bad_elections[e] = bad_senate_contests
        error_list = '\n'.join([
            '- {0} has {1}:\n{2}'.format(
                k, len(v), '\n'.join([' - %s' % c for c in v])
            ) for k, v in bad_elections.items()
        ])
        msg = '{0} elections with State Senate contests in the wrong districts:\n{1}'.format(
            len(bad_elections), error_list
        )

        return (len(bad_elections) == 0, msg)

    def test_for_duplicate_memberships(self):
        """
        Confirm there are no duplicate membership records.

        Return a tuple with boolean value (True means passed) and error message.
        """
        dupes = OCDMembershipProxy.objects.get_duplicates()
        error_list = '\n'.join([
            '- {0} in {1} repeated in {2} rows.'.format(
                i.person, i.post, i.row_count
            ) for i in dupes]
        )
        msg = '{0} duplicated Memberships:\n{1}'.format(dupes.count(), error_list)

        return (not dupes.exists(), msg)
