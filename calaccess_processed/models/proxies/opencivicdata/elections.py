#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from django.db.models import Count, Manager
from django.utils.text import get_text_list
from opencivicdata.elections.models import (
    Election,
    ElectionIdentifier,
    ElectionSource,
)
from postgres_copy import CopyQuerySet
from .base import OCDProxyModelMixin
from .candidatecontests import OCDCandidateContestProxy
from .divisions import OCDDivisionProxy
from .organizations import OCDOrganizationProxy
from .posts import OCDPostProxy


class OCDPartisanPrimaryManager(Manager):
    """
    Custom manager for limiting OCD elections querysets to partisan primaries.
    """
    def get_queryset(self):
        """
        Returns whether or not this was a primary election held in the partisan era prior to 2012.
        """
        return super(OCDPartisanPrimaryManager, self).get_queryset().filter(
            date__year__lt=2012,
            name__icontains='PRIMARY'
        )


class OCDElectionManager(Manager):
    """
    Custom helpers for the OCD Election model.
    """
    def create_from_calaccess(self, name, dt, election_id=None, election_type=None):
        """
        Create an OCD Election object.
        """
        # Create the object
        obj = self.get_queryset().create(
            name=name,
            date=dt,
            administrative_organization=OCDOrganizationProxy.objects.elections_division(),
            division=OCDDivisionProxy.objects.california(),
        )

        # And add the identifier so we can find it in the future
        if election_id:
            obj.identifiers.create(scheme='calaccess_election_id', identifier=election_id)

        # Add the election type so we can pull it out later if we want it.
        if election_type:
            obj.extras['calaccess_election_type'] = [election_type]
            obj.save()

        # Pass it back
        return obj


class OCDElectionProxy(Election, OCDProxyModelMixin):
    """
    A proxy on the OCD Election model.
    """
    objects = OCDElectionManager.from_queryset(CopyQuerySet)()
    partisan_primaries = OCDPartisanPrimaryManager()

    copy_to_fields = (
        ('id',),
        ('name',),
        ('date',),
        ('division_id',),
        ('administrative_organization_id',),
        ('created_at',),
        ('updated_at',),
        ('extras',),
        ('locked_fields',),
    )

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True

    def add_election_type(self, election_type):
        """
        Add election_type to 'calaccess_election_type' in extras field (if missing).
        """
        if 'calaccess_election_type' in self.extras.keys():
            # and if this one isn't included
            if election_type not in self.extras[
                'calaccess_election_type'
            ]:
                # then append
                self.extras['calaccess_election_type'].append(election_type)
                # and save
                self.save()
        else:
            # if election doesn't already have types, add the key
            self.extras['calaccess_election_type'] = [election_type]
            # and save
            self.save()

        return

    def add_election_id(self, election_id):
        """
        Add election_id to identifiers, if missing.
        """
        if not self.identifiers.filter(
            scheme='calaccess_election_id',
            identifier=election_id,
        ).exists():
            self.identifiers.create(
                scheme='calaccess_election_id',
                identifier=election_id,
            )
            self.save()

        return

    def get_regular_senate_contests_in_wrong_districts(self):
        """
        Get a list of regular senate contests in districts that shouldn't be contested.
        """
        if self.is_gubernatorial_election:
            # in gubernatorial elections,
            # odd-numbered senate districts should not contested
            contests = [
                c for c in self.senate_contests.regular()
                if int(c.division.subid2) % 2 != 0
            ]
        else:
            # in non-gubernatorial elections,
            # even-numbered senate districts should not be contests
            contests = [
                c for c in self.senate_contests.regular()
                if int(c.division.subid2) % 2 == 0
            ]
        return contests

    @property
    def assembly_contests(self):
        """
        State Assembly CandidateContests occurring in the election.
        """
        return self.candidate_contest_proxies.assembly()

    @property
    def candidate_contest_proxies(self):
        """
        A QuerySet of OCDCandidateContestProxy for the election.
        """
        return OCDCandidateContestProxy.objects.filter(election=self)

    @property
    def election_type(self):
        """
        Returns the primary CAL-ACCESS election type included with this record.
        """
        for et in self.extras.get('calaccess_election_type', []):
            if et in self.name:
                return et

    @property
    def election_types(self):
        """
        Returns all the CAL-ACCESS election types included with this record.
        """
        return self.extras.get('calaccess_election_type', [])

    @property
    def executive_contests(self):
        """
        State Executive Branch CandidateContests occurring in the election.
        """
        return self.candidate_contest_proxies.executive()

    @property
    def has_special_contests(self):
        """
        This election includes contests outside the regular election calendar.
        """
        special_election_types = set(
            ("SPECIAL ELECTION", "SPECIAL RUNOFF", "RECALL")
        )
        return len(
            special_election_types.intersection(self.election_types)
        ) > 0

    @property
    def identifier_list(self):
        """
        Returns a prettified list of OCD identifiers.
        """
        template = "{0.scheme}: {0.identifier}"
        return get_text_list([template.format(i) for i in self.identifiers.all()])

    @property
    def is_gubernatorial_election(self):
        """
        This election should include contests for Governor other executive branch offices.
        """
        # Governors are elected every four years, and the earliest such election
        # in CAL-ACCESS was 2002
        return (self.date.year - 2002) % 4 == 0

    @property
    def is_partisan_primary(self):
        """
        Returns whether or not this was a primary election held in the partisan era prior to 2012.
        """
        if 'PRIMARY' in self.election_types:
            if self.date.year < 2012:
                return True
        return False

    @property
    def regular_assembly_contest_count_actual(self):
        """
        Actual count of regular State Assembly contests.
        """
        return self.assembly_contests.regular().count()

    @property
    def regular_assembly_contest_count_expected(self):
        """
        Expected count of regular State Assembly contests (based on year).
        """
        assembly_office_count = OCDPostProxy.assembly.count()

        if "GENERAL" in self.election_types:
            expected_contest_count = assembly_office_count
        elif "PRIMARY" in self.election_types:
            if self.is_partisan_primary:
                # should be one contest for every distinct party in each
                # of the (80) assembly seats
                expected_contest_count = 0
                contests_q = self.assembly_contests.regular()
                contest_counts_by_party = contests_q.order_by().values(
                    'candidacies__party__name'
                ).annotate(
                    contest_count=Count('candidacies__contest', distinct=True)
                )
                for party in contest_counts_by_party:
                    expected_contest_count += party['contest_count']
            else:
                expected_contest_count = assembly_office_count
        else:
            expected_contest_count = 0

        return expected_contest_count

    @property
    def regular_executive_contest_count_actual(self):
        """
        Actual count of regular State Executive Branch contests.
        """
        return self.executive_contests.regular().count()

    @property
    def regular_executive_contest_count_expected(self):
        """
        Expected count of regular State Assembly contests (based on year).
        """
        exec_office_count = OCDPostProxy.executive.count()

        if self.is_gubernatorial_election:
            if "GENERAL" in self.election_types:
                expected_contest_count = exec_office_count
            elif "PRIMARY" in self.election_types:
                if self.is_partisan_primary:
                    # should be 1 contest for every distinct party in each
                    # of the executive branch offices (12)
                    expected_contest_count = 0
                    contests_q = self.executive_contests.regular()
                    contest_counts_by_party = contests_q.order_by().values(
                        'candidacies__party__name'
                    ).annotate(
                        contest_count=Count('candidacies__contest', distinct=True)
                    )
                    for party in contest_counts_by_party:
                        expected_contest_count += party['contest_count']
                else:
                    expected_contest_count = exec_office_count
            else:
                expected_contest_count = 0
        else:
            expected_contest_count = 0

        return expected_contest_count

    @property
    def regular_senate_contest_count_actual(self):
        """
        Actual count of regular State Senate contests.
        """
        return self.senate_contests.regular().count()

    @property
    def regular_senate_contest_count_expected(self):
        """
        Confirm the Election has the correct count of regular Assembly contests.
        """
        # half of the senates are filled every two years
        senate_office_count = int(OCDPostProxy.senate.count() / 2)

        if "GENERAL" in self.election_types:
            expected_contest_count = senate_office_count
        elif "PRIMARY" in self.election_types:
            if self.is_partisan_primary:
                # should be one contest for every distinct party in every
                # other senate district (20)
                expected_contest_count = 0
                contests_q = self.senate_contests.regular()
                contest_counts_by_party = contests_q.order_by().values(
                    'candidacies__party__name'
                ).annotate(
                    contest_count=Count('candidacies__contest', distinct=True)
                )
                for party in contest_counts_by_party:
                    expected_contest_count += party['contest_count']
            else:
                expected_contest_count = senate_office_count
        else:
            expected_contest_count = 0

        return expected_contest_count

    @property
    def senate_contests(self):
        """
        State Senate CandidateContests occurring in the election.
        """
        return self.candidate_contest_proxies.senate()

    @property
    def source_list(self):
        """
        Returns a prettified list of OCD sources.
        """
        return get_text_list(list(self.sources.all()))


class OCDElectionIdentifierProxy(ElectionIdentifier, OCDProxyModelMixin):
    """
    A proxy on the OCD ElectionIdentifier model.
    """
    objects = CopyQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True


class OCDElectionSourceProxy(ElectionSource, OCDProxyModelMixin):
    """
    A proxy on the OCD ElectionSource model.
    """
    objects = CopyQuerySet.as_manager()

    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
