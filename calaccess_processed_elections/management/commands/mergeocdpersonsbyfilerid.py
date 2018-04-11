#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find and merge OCD Person records that share the same CAL-ACCESS filer_id.
"""
from django.db.models import Count
from calaccess_processed_elections.merge import merge_persons
from opencivicdata.core.models import Person, PersonIdentifier
from calaccess_processed.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Find and merge OCD Person records that share the same CAL-ACCESS filer_id.
    """
    help = 'Find and merge OCD Person records that share the same CAL-ACCESS filer_id'

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

        if shared_filer_ids_q.count() == 0:
            self.log("No persons to merge by CAL-ACCESS filer_id")
        else:

            self.header(
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

                merge_persons(persons)

            self.success("Done!")
