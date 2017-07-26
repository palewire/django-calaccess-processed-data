#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Merge Persons that share the same CAL-ACCESS filer_id.
"""
from django.db.models import Count
from calaccess_processed.models import OCDPersonProxy
from calaccess_processed.management.commands import CalAccessCommand
from opencivicdata.core.models import Person, PersonIdentifier


class Command(CalAccessCommand):
    """
    Merge Persons that share the same CAL-ACCESS filer_id.
    """
    help = 'Merge Persons that share the same CAL-ACCESS filer_id'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        # Loop over all CAL-ACCESS filer_ids linked to multiple Persons
        shared_filer_ids_q = PersonIdentifier.objects.values(
            'identifier',
        ).annotate(
            person_count=Count('person'),
        ).filter(
            scheme='calaccess_filer_id',
            person_count__gt=1,
        ).order_by()

        self.log(
            "Merging %s Person sets with shared CAL-ACCESS filer_id" % shared_filer_ids_q.count()
        )

        for group in shared_filer_ids_q.all():
            persons = [
                p for p in Person.objects.filter(
                    identifiers__scheme='calaccess_filer_id',
                    identifiers__identifier=group['identifier'],
                ).all()
            ]

            if self.verbosity > 2:
                self.log(
                    "Merging {0} Persons sharing filer_id {1}".format(
                        len(persons),
                        group['identifier'],
                    )
                )

            OCDPersonProxy.objects.merge(persons)

        self.success("Done!")
