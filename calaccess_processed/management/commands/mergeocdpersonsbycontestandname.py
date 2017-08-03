#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find and merge OCD Person records that share a name and CandidateContest.
"""
from django.db.models import Count
from calaccess_processed.models import OCDPersonProxy
from opencivicdata.elections.models import CandidateContest
from calaccess_processed.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Find and merge OCD Person records that share a name and CandidateContest.
    """
    help = 'Find and merge OCD Person records that share a name and CandidateContest'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        self.header("Merging Persons in same Contest with shared name")

        # Loop over all CandidateContests
        for contest in CandidateContest.objects.all():
            for group_q in self.group_by_candidate_name(contest.candidacies):
                self.handle_group(group_q)

            for group_q in self.group_by_person_name(contest.candidacies):
                self.handle_group(group_q)

            for group_q in self.group_by_other_name(contest.candidacies):
                print('Grouped by other_name')
                print(group_q.count())
                print('--------------------------')
                self.handle_group(group_q)

        self.success("Done!")

    def group_by_candidate_name(self, candidacies_q):
        """
        Return a list of QuerySets for Candidacies with the same candidate_name.
        """
        q = candidacies_q.values('candidate_name').annotate(
            row_count=Count('id'),
        ).order_by().filter(row_count__gt=1)

        results = []

        for i in q.all():
            results.append(
                candidacies_q.filter(
                    candidate_name=i['candidate_name']
                ).order_by()
            )

        return results

    def group_by_person_name(self, candidacies_q):
        """
        Return a list of QuerySets for Candidacies with the same Person name.
        """
        q = candidacies_q.values('person__name').annotate(
            row_count=Count('id'),
        ).order_by().filter(row_count__gt=1)

        results = []

        for i in q.all():
            results.append(
                candidacies_q.filter(
                    person__name=i['person__name']
                ).order_by()
            )

        return results

    def group_by_other_name(self, candidacies_q):
        """
        Return a list of QuerySets for Candidacies with shared other_name.
        """
        # get the distinct count of person_ids for each other_name
        # linked to a person who's linked to one of the contest's candidacies
        q = candidacies_q.values('person__other_names__name').annotate(
            row_count=Count('person_id', distinct=True),
        ).order_by().filter(row_count__gt=1)

        results = []

        for i in q.all():
            if i['person__other_names__name']:
                results.append(
                    candidacies_q.filter(
                        person__other_names__name=i['person__other_names__name']
                    ).order_by()
                )

        return results

    def group_by_party(self, candidacies_q):
        """
        Return a list of QuerySets for Candidacies with the same party.
        """
        q = candidacies_q.values('party').annotate(
            row_count=Count('id'),
        ).order_by().filter(row_count__gt=1)

        results = []

        for i in q.all():
            results.append(
                candidacies_q.filter(
                    party=i['party']
                ).order_by()
            )

        return results

    def get_group_filer_id_count(self, candidacies_q):
        """
        Return the count of distinct filer_ids in the Candidacy QuerySet.
        """
        return candidacies_q.filter(
            person__identifiers__scheme='calaccess_filer_id'
        ).distinct('person__identifiers__identifier').count()

    def handle_group(self, group_q):
        """
        Handle group of candidates for merging.
        """
        # if there isn't more than one party and more than one filer_id
        if (
            group_q.distinct('party').exclude(party__isnull=True).count() <= 1 and
            self.get_group_filer_id_count(group_q) <= 1
        ):
            if self.verbosity > 2:
                self.log(
                    'Merging {0} persons in {1}'.format(
                        group_q.count(),
                        group_q.all()[0].contest,
                    )
                )
                for c in group_q.all():
                    self.log(' - {} ({})'.format(c.person, c.person_id))
            # merge
            OCDPersonProxy.objects.merge([c.person for c in group_q.all()])
        # handle multiple parties in the group
        elif group_q.distinct('party').count() > 1:
            # for each group with the same party in the group
            for party_group_q in self.group_by_party(group_q):
                # if there's only one filer_id
                if self.get_group_filer_id_count(party_group_q) <= 1:
                    # merge the group
                    OCDPersonProxy.objects.merge(
                        [c.person for c in party_group_q.all()]
                    )
        return
