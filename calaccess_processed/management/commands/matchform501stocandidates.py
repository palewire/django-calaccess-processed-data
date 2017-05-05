#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Supplement OCD Candidacy records with data from Form501Filings.
"""
from django.db.models import Value, CharField
from django.db.models.functions import Concat
from calaccess_processed.models import Form501Filing
from calaccess_processed.management.commands import CalAccessCommand
from opencivicdata.models import PersonIdentifier, Candidacy


class Command(CalAccessCommand):
    """
    Supplement OCD Candidacy records with data from Form501Filings.
    """
    help = 'Supplement OCD Candidacy records with data from Form501Filings.'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        for candidacy in Candidacy.objects.exclude(
            extras__has_key='form501filingid'
        ):
            if candidacy.post.role == 'Assembly Member':
                role = 'Assembly'
            elif candidacy.post.role == 'Senator':
                role = 'State Senate'
            else:
                role = candidacy.post.role

            if candidacy.contest.division.subid2 == '':
                district = None
            else:
                district = candidacy.contest.division.subid2

            try:
                filer_id = candidacy.person.identifiers.get(
                    scheme='calaccess_filer_id'
                )
            except PersonIdentifier.DoesNotExist:
                filer_id = None

            form501 = None

            if filer_id:
                try:
                    form501 = Form501Filing.objects.get(
                        filer_id=candidacy.person.identifiers.get(scheme='calaccess_filer_id'),
                        office=role,
                        district=district,
                        election_year=candidacy.election.start_time.year,
                    )
                except (
                    Form501Filing.DoesNotExist,
                    Form501Filing.MultipleObjectsReturned
                ):
                    pass

            if not form501:
                try:
                    form501 = Form501Filing.objects.annotate(
                        full_name=Concat(
                            'last_name',
                            Value(', '),
                            'first_name',
                            output_field=CharField(),
                        ),
                    ).get(
                        full_name=candidacy.person.sort_name,
                        office=role,
                        district=district,
                        election_year=candidacy.election.start_time.year,
                    )
                except Form501Filing.MultipleObjectsReturned:
                    form501 = None
                except Form501Filing.DoesNotExist:
                    try:
                        form501 = Form501Filing.objects.annotate(
                            full_name=Concat(
                                'last_name',
                                Value(', '),
                                'first_name',
                                'middle_name',
                                output_field=CharField(),
                            ),
                        ).get(
                            full_name=candidacy.person.sort_name,
                            office=role,
                            district=district,
                            election_year=candidacy.election.start_time.year,
                        )
                    except (
                        Form501Filing.DoesNotExist,
                        Form501Filing.MultipleObjectsReturned
                    ):
                        form501 = None

            if form501:
                candidacy.extras = {'form501filingid': form501.filing_id}
                candidacy.save()

        self.success("Done!")
