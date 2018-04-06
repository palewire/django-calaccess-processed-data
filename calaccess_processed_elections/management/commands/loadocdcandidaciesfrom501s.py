#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load the OCD Candidacy model with data extracted from the Form501Filing model.
"""
from __future__ import unicode_literals
from django.core.management.base import CommandError
from opencivicdata.elections.models import CandidateContest
from calaccess_processed.management.commands import CalAccessCommand
from calaccess_processed.models import Form501Filing, OCDCandidacyProxy


class Command(CalAccessCommand):
    """
    Load the OCD Candidacy model with data extracted from the Form501Filing model.
    """
    help = 'Load the OCD Candidacy model with data extracted from the Form501Filing model'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        if not CandidateContest.objects.exists():
            error_message = 'No contests currently loaded (run loadocdcandidatecontests).'
            if self._called_from_command_line:
                self.failure(error_message)
            else:
                raise CommandError(error_message)
        else:
            form501_count = Form501Filing.objects.without_candidacy().count()
            self.header(
                "Processing %s Form 501 filings without candidacies" % form501_count
            )
            self.load()

        self.success("Done!")

    def load(self):
        """
        Loop over each Form501Filing and attempt to load into OCD models.
        """
        for form501 in Form501Filing.objects.without_candidacy():
            if self.verbosity > 2:
                self.log(' Processing Form 501: %s' % form501.filing_id)
                self.process_form501(form501)

    def process_form501(self, form501):
        """
        Process a Form501Filing and attempt to load its data into OCD models.
        """
        # Get a linked contest
        contest = form501.get_or_create_contest()

        # If there is no contest, skip.
        if not contest:
            pass
        else:
            candidacy, created = OCDCandidacyProxy.objects.get_or_create_from_calaccess(
                contest,
                form501.parsed_name,
                candidate_filer_id=form501.filer_id
            )

            if created and self.verbosity > 2:
                self.log(' Created Candidacy: %s' % candidacy)

            candidacy.link_form501(form501.filing_id)
            candidacy.update_from_form501()
            candidacy.update_party_from_form501()

        return form501
