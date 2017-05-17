#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Merge Persons that share the same CAL-ACCESS filer_id.
"""
from django.db.models import Count
from calaccess_processed.management.commands import LoadOCDModelsCommand
from opencivicdata.models import Person, PersonIdentifier
from opencivicdata.models.merge import merge


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

        self.header(
            "Merging %s Person sets with shared CAL-ACCESS filer_id" % shared_filer_ids_q.count()
        )

        for filer_id in shared_filer_ids_q.all():
            # get the persons with that filer_id
            persons = Person.objects.filter(
                identifiers__scheme='calaccess_filer_id',
                identifiers__identifier=filer_id['identifier'],
            ).all()
            # each person will be merged into this one
            survivor = persons[0]

            # loop over all the rest of them
            for i in range(1, filer_id['person_count']):
                if survivor.id != persons[i].id:
                    merge(survivor, persons[i])

            # also delete the now duplicated PersonIdentifier objects
            if survivor.identifiers.count() > 1:
                for i in survivor.identifiers.filter(scheme='calaccess_filer_id')[1:]:
                    i.delete()

        self.success("Done!")
