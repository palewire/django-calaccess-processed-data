#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find and merge OCD Person records that share a name and CandidateContest.
"""
from django.db.models import Count
from calaccess_processed_elections.merge import merge_persons
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed_elections.proxies import OCDCandidateContestProxy


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
        for contest in OCDCandidateContestProxy.objects.all():
            # handle groups by candidate_name
            for group_q in self.group_by_candidate_name(contest.candidacies):
                self.handle_group(group_q, field_name='candidate_name')
            # handle groups by person_name
            for group_q in self.group_by_person_name(contest.candidacies):
                self.handle_group(group_q, field_name='person_name')
            # handle groups by person_other_name
            for group_q in self.group_by_other_name(contest.candidacies):
                self.handle_group(group_q, field_name='other_name')

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

    def log_merged_persons(self, group_q, field_name):
        """
        Log the persons in group_q who will be merged.
        """
        self.log(
            'Merging {0} persons grouped by {1} in {2}'.format(
                group_q.count(),
                field_name,
                group_q.all()[0].contest,
            )
        )
        for c in group_q.all():
            self.log(' - {} ({})'.format(c.person, c.person_id))

    def handle_group(self, group_q, field_name=None):
        """
        Handle merging of candidates in group_q.

        Optional field_name is a string naming the field used to form the group.
        """
        # if there isn't more than one party and more than one filer_id
        if (
            group_q.distinct('party').exclude(party__isnull=True).count() <= 1
            and self.get_group_filer_id_count(group_q) <= 1
        ):
            if self.verbosity > 2:
                self.log_merged_persons(group_q, field_name)
            # merge
            merge_persons([c.person for c in group_q.all()])
        # handle multiple parties in the group
        elif group_q.distinct('party').count() > 1:
            # for each group with the same party in the group
            for party_group_q in self.group_by_party(group_q):
                # if there's only one filer_id
                if self.get_group_filer_id_count(party_group_q) <= 1:
                    if self.verbosity > 2:
                        self.log_merged_persons(party_group_q, field_name)
                    # merge the group
                    merge_persons(
                        [c.person for c in party_group_q.all()]
                    )
        return
