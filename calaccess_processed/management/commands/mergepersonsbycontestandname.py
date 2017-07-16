#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Merge duplicate Candidacies within the same CandidateContest.
"""
from django.db.models import Count
from calaccess_processed.management.commands import LoadOCDModelsCommand
from opencivicdata.elections.models import CandidateContest


class Command(LoadOCDModelsCommand):
    """
    Merge duplicate Candidacies within the same CandidateContest.
    """
    help = 'Merge duplicate Candidacies within the same CandidateContest.'

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
        q = candidacies_q.values('person__other_names__name').annotate(
            row_count=Count('id'),
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
                    self.log(' - {}'.format(c.person))
            # merge
            self.merge_persons([c.person for c in group_q.all()])
        # handle multiple parties in the group
        elif group_q.distinct('party').count() > 1:
            # for each group with the same party in the group
            for party_group_q in self.group_by_party(group_q):
                # if there's only one filer_id
                if self.get_group_filer_id_count(party_group_q) <= 1:
                    # merge the group
                    self.merge_persons(
                        [c.person for c in party_group_q.all()]
                    )
        return
