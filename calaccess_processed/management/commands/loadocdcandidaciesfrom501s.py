#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load the Candidacy models from records extracted from Form501Filings.
"""
from __future__ import unicode_literals
from datetime import date
from calaccess_processed import corrections
from opencivicdata.core.models import Division
from django.core.management.base import CommandError
from opencivicdata.elections.models import CandidateContest
from calaccess_raw.models import FilerToFilerTypeCd, LookupCodesCd
from calaccess_processed.management.commands import LoadOCDModelsCommand
from calaccess_processed.models import Form501Filing, OCDPartyProxy, OCDPostProxy


class Command(LoadOCDModelsCommand):
    """
    Load the Candidacy models from records extracted from Form501Filings.
    """
    help = 'Load the Candidacy models from records extracted from Form501Filings.'

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
            self.header("Loading additional candidacies from Form 501 filings")

            for form501 in Form501Filing.objects.without_candidacy():
                if self.verbosity > 2:
                    self.log(' Processing Form 501: %s' % form501.filing_id)
                self.process_form501(form501)

            self.success("Done!")

    def process_form501(self, form501):
        """
        Extract data from Form501Filing and load into OCD models.
        """
        # Get the election
        election = form501.ocd_election

        # If there is no linked election, just give up
        if not election:
            return None

        # Get a linked contest
        contest = form501.get_contest()

        # If there is no contest, quit.
        if not contest:
            return None

        # candidacy, candidacy_created = self.get_or_create_candidacy(
        #     contest,
        #     sort_name,
        #     # registration status: these are the "uncertified" who did not qualify
        #     'filed',
        #     filer_id=form501.filer_id,
        # )
        #
        # if candidacy_created and self.verbosity > 2:
        #     tmp = ' Created new Candidacy: {0.candidate_name} in {0.post.label}'
        #     self.log(tmp.format(candidacy))
        #
        # candidacy.party = self.get_party_from_form501(
        #     form501,
        #     contest.election.date
        # )
        # candidacy.save()
        # self.link_form501_to_candidacy(form501.filing_id, candidacy)
        # self.update_candidacy_from_form501s(candidacy)
