#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load the Candidacy models from records extracted from Form501Filings.
"""
from calaccess_raw.models import FilerToFilerTypeCd, LookupCodesCd
from calaccess_processed.management.commands import LoadOCDModelsCommand
from calaccess_processed.models import Form501Filing
from opencivicdata.models import (
    CandidateContest,
    Candidacy,
    Division,
    Election,
)


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
        self.header("Loading additional candidacies from Form 501 filings")
        self.load()
        self.success("Done!")

    def get_election(self, year, election_type):
        """
        Return Election occurring in year with name in including election_type.

        Return None if none found.
        """
        try:
            election = Election.objects.get(
                start_time__year=year,
                name__contains=election_type,
            )
        except (Election.DoesNotExist, Election.MultipleObjectsReturned):
            election = None

        return election

    def lookup_office_for_filer_id(self, filer_id, election_date):
        """
        Lookup the office for the given filer_id, effective before election_date.

        Return a string containg the office name and district number (if applicable),
        or None if not found.
        """
        try:
            ftft = FilerToFilerTypeCd.objects.filter(
                filer_id=filer_id,
                effect_dt__lte=election_date,
            ).latest('effect_dt')
        except FilerToFilerTypeCd.DoesNotExist:
            result = None
        else:
            try:
                office = LookupCodesCd.objects.get(
                    code_id=ftft.race
                )
            except LookupCodesCd.DoesNotExist:
                result = None
            else:
                if ftft.district_cd and ftft.district_cd != 0:
                    try:
                        district = LookupCodesCd.objects.get(
                            code_id=ftft.district_cd
                        )
                    except LookupCodesCd.DoesNotExist:
                        district = None

                result = '{0} {1}'.format(office, district).strip()

        return result

    def get_post_from_form501(self, form501, election):
        """
        Get a Post using data extracted from Form501Filing.

        Return Post object or None if not found.
        """
        post = None
        office_name = '{0.office} {0.district}'.format(form501).strip()

        try:
            post = self.get_or_create_post(
                office_name,
                get_only=True,
            )[0]
        except Division.DoesNotExist:
            # try extracting office and district from FilerToFilerTypeCd
            office_name = self.lookup_office_for_filer_id(
                form501.filer_id,
                election.start_time.date(),
            )
            if office_name:
                try:
                    post = self.get_or_create_post(
                        office_name,
                        get_only=True,
                    )[0]
                except Division.DoesNotExist:
                    pass

        return post

    def get_party_from_form501(self, form501, election_date):
        """
        Get the Party from Form501Filing.

        Return Party object or None.
        """
        party = self.lookup_party(form501.party)
        # if unable to match form501 party, try looking in FilerToFilerTypes
        if not party:
            party = self.get_party_for_filer_id(
                int(form501.filer_id),
                election_date,
            )

        return party

    def get_contest_from_form501(self, form501, election):
        """
        Get CandidateContest by extracting info form Form501Filing.

        Return a CandidateContest or None.
        """
        post = self.get_post_from_form501(form501, election)

        # Don't bother trying to get contest unless we have a post
        if not post:
            contest = None
        else:
            contest_data = {
                'posts__post': post,
                'division': post.division,
                'election': election,
            }
            # if looking for a pre-2012 primary, include party
            if election.start_time.year < 2012 and 'PRIMARY' in election.name:
                contest_data['party'] = self.get_party_from_form501(
                    form501,
                    election.start_time.date()
                )

            try:
                contest = CandidateContest.objects.get(**contest_data)
            except CandidateContest.DoesNotExist:
                contest = None

        return contest

    def process_form501(self, form501):
        """
        Extract data from Form501Filing and load into OCD models.
        """
        # Get the election
        if form501.election_year and form501.election_type:
            election = self.get_election(
                form501.election_year,
                form501.election_type
            )
        else:
            election = None

        if election:
            contest = self.get_contest_from_form501(form501, election)

            if contest:
                # "terminated" statement type
                if form501.statement_type == '10003':
                    registration_status = 'withdrawn'
                else:
                    # these are the "uncertified" who did not qualify
                    registration_status = 'filed'

                # format the name
                name = '{0.last_name}, {0.first_name} {0.middle_name}'.format(
                    form501
                ).strip()
                # Create the Candidacy
                candidacy, candidacy_created = self.get_or_create_candidacy(
                    contest,
                    filer_id=form501.filer_id,
                    person_name=name,
                    registration_status=registration_status,
                )

                if candidacy_created and self.verbosity > 2:
                    tmp = ' Created new Candidacy: {0.candidate_name} in {0.post.label}'
                    self.log(tmp.format(candidacy))

                candidacy.party = self.get_party_from_form501(
                    form501,
                    contest.election.start_time.date()
                )
                candidacy.extras = {'form501filingid': form501.filing_id}
                candidacy.filed_date = form501.date_filed
                candidacy.save()
        return

    def load(self):
        """
        Loop over unmatched Form501Filings, creating Candidacy objects.
        """
        candidacies_w_form501_q = Candidacy.objects.filter(
            extras__has_key='form501filingid'
        ).values('extras')

        unmatched_form501s_q = Form501Filing.objects.exclude(
            filing_id__in=[
                i['extras']['form501filingid'] for i in candidacies_w_form501_q
            ]
        )

        for form501 in unmatched_form501s_q.all():
            if self.verbosity > 2:
                self.log(' Processing Form 501: %s' % form501.filing_id)
                self.log(' See filing at: %s' % form501.pdf_url)
            self.process_form501(form501)

        return
