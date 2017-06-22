#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Merge Persons that share the same CAL-ACCESS filer_id.
"""
from django.db.models import Count
from calaccess_processed.management.commands import LoadOCDModelsCommand
from opencivicdata.core.models import PersonIdentifier


class Command(LoadOCDModelsCommand):
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
        )

        self.log(
            "Merging %s Person sets with shared CAL-ACCESS filer_id" % shared_filer_ids_q.count()
        )

        for filer_id in shared_filer_ids_q.all():
            self.merge_persons(filer_id['identifier'])

        self.success("Done!")
