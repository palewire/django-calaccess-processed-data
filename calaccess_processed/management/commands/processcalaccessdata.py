#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load data into processed CAL-ACCESS models, archive processed files and ZIP.
"""
from django.apps import apps
from django.core.management import call_command
from calaccess_processed.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Load data into processed CAL-ACCESS models, archive processed files and ZIP.
    """
    help = 'Load data into processed CAL-ACCESS models, archive processed files and ZIP.'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        call_command(
            'loadcalaccessfilingmodels',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )

        call_command(
            'loadparties',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )

        call_command(
            'loadballotmeasurecontests',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )

        call_command(
            'loadretentioncontests',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )

        call_command(
            'loadincumbentofficeholders',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )

        call_command(
            'loadcandidatecontests',
            verbosity=self.verbosity,
            no_color=self.no_color,
        )

        # Archive OCD models
        ocd_models = [
            m for m in apps.get_app_config('opencivicdata').get_models()
            if not m._meta.abstract and
            m.objects.count() > 0
        ]

        for m in ocd_models:
            call_command(
                'archivecalaccessprocessedfile',
                'opencivicdata',
                m._meta.object_name,
            )
