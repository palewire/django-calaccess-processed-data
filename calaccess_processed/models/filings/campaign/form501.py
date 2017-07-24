#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing campaign-related entities derived from raw CAL-ACCESS data.
"""
from __future__ import unicode_literals
import itertools
from datetime import date
import calaccess_processed
from django.db import models
from django.db.models import Q
from calaccess_processed import corrections
from opencivicdata.elections.models import CandidateContest
from calaccess_processed.managers import ProcessedDataManager
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models import CalAccessBaseModel
from calaccess_processed.models.filings import FilingMixin, FilingVersionMixin


class Form501FilingManager(ProcessedDataManager):
    """
    A custom manager for Form 501 filings.
    """
    def without_candidacy(self):
        """
        Returns Form 501 filings that do not have an OCD Candidacy yet.
        """
        from calaccess_processed.models import OCDCandidacyProxy
        matched_qs = OCDCandidacyProxy.objects.matched_form501_ids()
        matched_list = [i for i in itertools.chain.from_iterable(matched_qs)]
        return self.get_queryset().exclude(filing_id__in=matched_list, office__icontains='RETIREMENT')


class Form501FilingBase(CalAccessBaseModel):
    """
    Base and abstract model for Form 501 filings.
    """
    date_filed = models.DateField(
        verbose_name='from date',
        null=True,
        db_index=True,
        help_text="Date when the Form 501 filing was filed (from F501_502_CD"
                  ".RPT_DATE)",
    )
    statement_type = models.CharField(
        max_length=62,
        verbose_name='statement type',
        help_text='Describes the type of statement, e.g. "ORIGINAL", "AMENDMENT" '
                  '(from LOOKUP_CODES.CODE_DESC)',
    )
    filer_id = models.CharField(
        verbose_name="filer identifier",
        max_length=9,
        help_text="Filer's unique identifier (from F501_502_CD.FILER_ID)",
    )
    committee_id = models.CharField(
        verbose_name='committee identifier',
        max_length=9,
        help_text="Candidate's committee's unique filer idenitifier (from "
                  "F501_502_CD.COMMITTEE_ID)",
    )
    title = models.CharField(
        verbose_name="candidate name title",
        max_length=100,
        blank=True,
        help_text="Name title of the candidate (from F501_502_CD.CAND_NAMT)",
    )
    last_name = models.CharField(
        verbose_name="candidate last name",
        max_length=200,
        # just a few don't even have a last name
        blank=True,
        help_text="Last name of the candidate (from F501_502_CD.CAND_NAML)",
    )
    first_name = models.CharField(
        verbose_name="candidate first name",
        max_length=45,
        blank=True,
        help_text="First name of the candidate (from F501_502_CD.CAND_NAMF)",
    )
    middle_name = models.CharField(
        verbose_name="candidate middle name",
        max_length=20,
        blank=True,
        help_text="Middle name of the candidate (from F501_502_CD.CAND_NAMM)",
    )
    name_suffix = models.CharField(
        verbose_name="candidate name suffix",
        max_length=10,
        blank=True,
        help_text="Name suffix of the candidate (from F501_502_CD.CAND_NAMS)",
    )
    name_moniker = models.CharField(
        verbose_name="candidate name moniker",
        max_length=20,
        blank=True,
        help_text="Moniker (aka, nickname) of the candidate (from F501_502_CD"
                  ".MONIKER)",
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='candidate phone number',
        blank=True,
        help_text="Phone number of the candidate (from F501_502_CD.CAND_PHON)",
    )
    fax = models.CharField(
        max_length=20,
        verbose_name='fax number',
        blank=True,
        help_text="Phone number of the candidate (from F501_502_CD.CAND_FAX)",
    )
    email = models.CharField(
        max_length=200,
        verbose_name='email address',
        blank=True,
        help_text="Email address of the candidate (from F501_502_CD.CAND_EMAIL)",
    )
    city = models.CharField(
        max_length=200,
        verbose_name="candidate city",
        blank=True,
        help_text="City of the candidate (from F501_502_CD.CAND_CITY)",
    )
    state = models.CharField(
        max_length=200,
        verbose_name='candidate state',
        blank=True,
        help_text="State of the candidate (from F501_502_CD.CAND_ST)",
    )
    zip_code = models.CharField(
        max_length=10,
        verbose_name='zip code',
        blank=True,
        help_text='Zip code (usually zip5, sometimes zip9) of the '
                  'candidate (from F501_502_CD.CAND_ZIP4)',
    )
    office = models.CharField(
        verbose_name='office sought',
        max_length=80,
        blank=True,
        help_text='Position title of the office sought by the candidate (from '
                  'LOOKUP_CODES_CD.CODE_DESC, unless NULL or 0, then F501_502_CD.'
                  'OFFICE_DSCR)',
    )
    agency = models.CharField(
        verbose_name='agency name',
        max_length=200,
        blank=True,
        help_text='Name of the agency with the office sought (from '
                  'F501_502_CD.AGENCY_NAM)',
    )
    district = models.IntegerField(
        verbose_name='district',
        null=True,
        help_text='District of office sought, if applicable (from LOOKUP_CODES_CD'
                  '.CODE_DESC, unless NULL or 0, then F501_502_CD.DIST_NO)',
    )
    party = models.CharField(
        max_length=30,
        verbose_name='political party',
        blank=True,
        help_text='Political party of the candidate (from LOOKUP_CODES_CD.'
                  'CODE_DESC, unless NULL or 0, then F501_502_CD.PARTY)',
    )

    jurisdiction = models.CharField(
        max_length=30,
        verbose_name='jurisdiction',
        blank=True,
        help_text='Jurisdiction of the office sought, e.g., "LOCAL", "STATE" '
                  '(from LOOKUP_CODES_CD.CODE_DESC)',
    )
    election_type = models.CharField(
        verbose_name='election type',
        max_length=16,
        null=True,
        help_text='Type of election in which the candidate is declaring intention'
                  ' to run, e.g. "PRIMARY", "GENERAL" (from LOOKUP_CODES_CD.'
                  'CODE_DESC)',
    )
    election_year = models.IntegerField(
        verbose_name='election year',
        null=True,
        help_text='Year in which the election is held (from F501_502_CD.YR_OF_ELEC)',
    )
    accepted_limit = models.NullBooleanField(
        null=True,
        help_text='Indicates if either the "I accept the voluntary expenditure '
                  'ceiling" or "I do not accept the voluntary expenditure" '
                  'box is checked (from F501_502_CD.ACCEPT_LIMIT_YN)',
    )
    limit_not_exceeded_election_date = models.DateField(
        verbose_name='limit not exceeded election date',
        null=True,
        help_text='Date of the primary or special election in which the candidate '
                  'did not accept the voluntary expenditure ceiling but also did '
                  'exceed the ceiling. Candidates may amend their Form 501 to accept '
                  'the limits for the general election or special election runoff '
                  'and receive all the benefits of accepting the ceiling (from '
                  'F501_502_CD.DID_EXCEED_DT)'
    )
    personal_funds_contrib_date = models.DateField(
        verbose_name='personal funds contribution date',
        null=True,
        help_text='Date on which the candidate contributed personal funds in excess '
                  'of the voluntary expenditure ceiling for the (from F501_502_CD'
                  '.CNTRB_PRSNL_FNDS_DT)',
    )
    executed_on = models.DateField(
        verbose_name='executed on date',
        null=True,
        help_text='Date on which the candidate intention statement was signed '
                  '(from F501_502_CD.EXECUTE_DT)'
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class Form501Filing(FilingMixin, Form501FilingBase):
    """
    The most recent version of each Form 501 filing by a candidate.

    Includes information from the most recent version of each Form 501 filing.
    All versions of the filings can be found in Form501FilingVersion.
    """
    filing_id = models.IntegerField(
        verbose_name='filing id',
        primary_key=True,
        null=False,
        help_text='Unique identification number for the Form 501 filing ('
                  'from F501_502_CD.FILING_ID)',
    )
    amendment_count = models.IntegerField(
        verbose_name='Count amendments',
        db_index=True,
        null=False,
        help_text='Number of amendments to the Form 501 filing (from '
                  'maximum value of F501_502_CD.AMEND_ID)',
    )
    objects = Form501FilingManager()

    class Meta:
        """
        Model options.
        """
        index_together = ((
            'filing_id',
            'amendment_count',
        ),)
        verbose_name = "Form 501 (Candidate Intention) filing"

    def __str__(self):
        return str(self.filing_id)

    @property
    def sort_name(self):
        """
        Return the 'sort_name' of the candidate to match the format we typically scrape from the CAL-ACCESS website.

        This is useful when trying to consolidate these forms with scraped data in our OCD models.
        """
        return '{0.last_name}, {0.first_name} {0.middle_name}'.format(self).strip()

    @property
    def office_name(self):
        """
        Return the 'office_name' of the candidate to match the format we typically scrape from the CAL-ACCESS website.

        This is useful when trying to consolidate these forms with scraped data in our OCD models.
        """
        return '{0.office} {0.district}'.format(self).strip()

    @property
    def ocd_election(self):
        """
        Return Election occurring in year with name in including election_type.

        Return None if none found.
        """
        from calaccess_processed.models import OCDElectionProxy

        if not self.election_year or not self.election_type:
            return None
        try:
            return OCDElectionProxy.objects.get(
                date__year=self.election_year,
                name__contains=self.election_type,
            )
        except (OCDElectionProxy.DoesNotExist, OCDElectionProxy.MultipleObjectsReturned):
            # if it's a future primary, try to calculate the date
            if self.election_year >= date.today().year and self.election_type == 'PRIMARY':
                try:
                    dt_obj = calaccess_processed.get_expected_election_date(self.election_year, self.election_type)
                except:
                    return None
                return OCDElectionProxy.objects.create_with_name_and_date(
                    '{0} {1}'.format(self.election_year, self.election_type),
                    dt_obj,
                )
            else:
                return None

    def get_party(self):
        """
        Get the Party from Form501Filing.

        Return Party object or None.
        """
        from calaccess_processed.models import OCDPartyProxy

        # first try the corrections
        party = corrections.candidate_party(
            '{0.last_name}, {0.first_name} {0.middle_name}'.format(self).strip(),
            self.election_year,
            self.election_type,
            '{0.office} {0.district}'.format(self).strip(),
        )
        if party:
            return party

        # then try using the party on the form501
        party = OCDPartyProxy.objects.get_by_name(self.party)
        if not party.is_unknown():
            return party

        # finally, try looking in FilerToFilerTypes
        ocd_election = self.ocd_election
        if not ocd_election:
            return OCDPartyProxy.objects.unknown()
        return OCDPartyProxy.objects.get_by_filer_id(int(self.filer_id), ocd_election.date)

    def get_contest(self):
        """
        Get CandidateContest by extracting info form Form501Filing.

        Return a CandidateContest or None.
        """
        from calaccess_processed.models import OCDPostProxy

        # Get election
        ocd_election = self.ocd_election
        if not ocd_election:
            return None

        # Get or create a post
        post = OCDPostProxy.objects.get_by_form501(self)

        # Don't bother trying to get contest unless we have a post
        if not post:
            return None

        # Seed contest data
        contest_data = {
            'posts__post': post,
            'division': post.division,
            'election': ocd_election,
        }

        # if looking for a pre-2012 primary, include party
        if ocd_election.is_partisan_primary():
            contest_data['party'] = self.get_party()

        # Try to get it from the database
        try:
            return CandidateContest.objects.get(**contest_data)
        except CandidateContest.DoesNotExist:
            # if the election date is later than today, but no contest
            if ocd_election.date > date.today():
                # make the contest (CAL-ACCESS website might behind)
                contest = CandidateContest.objects.create(
                    name=post.label.upper(),
                    division=contest_data['division'],
                    election=contest_data['election'],
                )
                contest.posts.create(
                    contest=contest,
                    post=contest_data['posts__post'],
                )
                return contest
            # Otherwise give up
            else:
                return None

    def get_or_create_candidacy(self, contest, registration_status='filed'):
        """
        Get or create a Candidacy object.
        """
        from calaccess_processed.models import OCDCandidacyProxy, OCDPersonProxy

        # If a filer_id is not provided, use the candidate's scraped id
        filer_id = self.filer_id or None

        name = self.sort_name
        candidacy = None

        # first, try matching to existing candidate in contest with filer_id
        if filer_id:
            try:
                candidacy = OCDCandidacyProxy.objects.filter(contest=contest).get(
                    person__identifiers__scheme='calaccess_filer_id',
                    person__identifiers__identifier=filer_id,
                )
            except OCDCandidacyProxy.DoesNotExist:
                pass
            else:
                candidacy_created = False
                # if provided name not person's current name and not linked to person add it
                if candidacy.person.name != name:
                    if not candidacy.person.other_names.filter(name=name).exists():
                        candidacy.person.other_names.create(
                            name=name,
                            note='Matched on CandidateContest and calaccess_filer_id'
                        )

        # if filer_id match fails (or no filer_id), try matching to candidate
        # in contest with provided name
        if not candidacy:
            try:
                candidacy = OCDCandidacyProxy.objects.filter(contest=contest).get(
                    Q(candidate_name=name) |
                    Q(person__name=name) |
                    Q(person__other_names__name=name)
                )
            except OCDCandidacyProxy.MultipleObjectsReturned:
                # weird case when someone filed for the same race
                # with three different filer_ids
                if self.sort_name == 'MC NEA, DOUGLAS A.':
                    candidacy = None
            except OCDCandidacyProxy.DoesNotExist:
                pass
            else:
                candidacy_created = False
                # if filer_id provided
                if filer_id:
                    # check to make sure candidate with same name doesn't have diff filer_id
                    has_diff_filer_id = candidacy.person.identifiers.filter(
                        scheme='calaccess_filer_id',
                    ).exists()
                    if has_diff_filer_id:
                        # if so, don't conflate
                        candidacy = None
                    else:
                        # if so, add filer_id to existing candidate
                        candidacy.person.identifiers.create(
                            scheme='calaccess_filer_id',
                            identifier=filer_id,
                        )

        # if no matched candidate yet, make a new one
        if not candidacy:
            # First make a Person object
            person, person_created = self.get_or_create_person()

            # if provided name not person's current name or other_name
            if person.name != name:
                if not person.other_names.filter(name=name).exists():
                    person.other_names.create(
                        name=name,
                        note='From %s candidacy' % contest
                    )

            # Then make the candidacy
            candidacy = OCDCandidacyProxy.objects.create(
                contest=contest,
                person=person,
                post=contest.posts.all()[0].post,
                candidate_name=name,
                registration_status=registration_status,
            )
            candidacy_created = True

        # if provided registration does not equal the default, update
        if registration_status != 'filed':
            candidacy.registration_status = registration_status
            candidacy.save()

        # make sure Person name is same as most recent candidate_name
        person = candidacy.person
        person.refresh_from_db()
        person.__class__ = OCDPersonProxy
        person.update_name()

        return candidacy, candidacy_created

    def get_or_create_person(self):
        """
        Get or create a Person object with the name string and optional filer_id.

        If a filer_id is provided, first attempt to lookup the Person by filer_id.
        If matched, and the provided name doesn't match the current name of the Person
        and isn't included in the other names of the Person, add it as an other_name.

        If the person doesn't exist (or the filer_id is not provided), create a
        new Person.

        Returns a tuple (Person object, created), where created is a boolean
        specifying whether a Person was created.
        """
        from calaccess_processed.models import OCDPersonProxy

        split_name = self.sort_name.split(',')
        split_name.reverse()
        name = ' '.join(split_name).strip()

        # If a filer_id is not provided, use the candidate's scraped id
        filer_id = self.filer_id or None

        if filer_id:
            try:
                person = OCDPersonProxy.objects.get(
                    identifiers__scheme='calaccess_filer_id',
                    identifiers__identifier=filer_id,
                )
            except OCDPersonProxy.DoesNotExist:
                pass
            else:
                # If we find a match, make sure it has this name variation logged
                if person.name != self.sort_name:
                    if not person.other_names.filter(name=self.sort_name).exists():
                        person.other_names.create(
                            name=self.sort_name,
                            note='Matched on calaccess_filer_id'
                        )
                # Then pass it out.
                return person, False

        # Otherwise create a new one
        person = OCDPersonProxy.objects.create(
            name=name,
            sort_name=self.sort_name,
        )
        if filer_id:
            person.identifiers.create(
                scheme='calaccess_filer_id',
                identifier=filer_id,
            )
        return person, True


@python_2_unicode_compatible
class Form501FilingVersion(FilingVersionMixin, Form501FilingBase):
    """
    Every version of each Form 501 (Candidate Intention Statement) filing by candidates.

    Includes information found on each version of each Form 501 filing. For the
    most recent version of each filing, see Form501Filing.
    """
    filing = models.ForeignKey(
        'Form501Filing',
        related_name='versions',
        db_constraint=False,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Unique identification number for the Form 501 filing ('
                  'from F501_502_CD.FILING_ID)',
    )
    amend_id = models.IntegerField(
        verbose_name='amendment id',
        null=False,
        help_text='Identifies the version of the Form 501 filing, with 0 '
                  'representing the initial filing (from F501_502_CD.FILING_ID)',
    )

    objects = ProcessedDataManager()

    class Meta:
        """
        Model options.
        """
        unique_together = ((
            'filing',
            'amend_id',
        ),)
        index_together = ((
            'filing',
            'amend_id',
        ),)
        verbose_name = "Form 501 (Candidate Intention) filing version"

    def __str__(self):
        return '{}-{}'.format(self.filing, self.amend_id)
