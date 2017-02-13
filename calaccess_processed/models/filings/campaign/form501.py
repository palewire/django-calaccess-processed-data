#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing campaign-related entities derived from raw CAL-ACCESS data.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.filings import (
    FilingMixin,
    FilingVersionMixin,
)
from calaccess_processed.managers import ProcessedDataManager


class Form501FilingBase(models.Model):
    """
    Base and abstract model for Form 460 filings.
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

    objects = ProcessedDataManager()

    class Meta:
        """
        Model options.
        """
        index_together = ((
            'filing_id',
            'amendment_count',
        ),)

    def __str__(self):
        return str(self.filing_id)


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

    def __str__(self):
        return '%s-%s' % (self.filing, self.amend_id)


@python_2_unicode_compatible
class Candidate(models.Model):
    """
    Name, office/district/agency sought and contact info of each candidate.

    Derived from filers of Form 501 (Candidate Intention Statement).
    """
    filer_id = models.IntegerField(
        verbose_name="filer ID",
        null=False,
        help_text="Filer's unique id translated to numeric form (via "
                  "FILER_XREF_CD). In cases without an XREF translation, "
                  "the F501 filer_id is simply cast as an integer.",
    )
    title = models.CharField(
        verbose_name="name title",
        max_length=100,
        null=False,
        blank=True,
        help_text="Candidate's name title",
    )
    last_name = models.CharField(
        verbose_name="last name",
        max_length=200,
        null=False,
        # just a few don't even have a last name
        blank=True,
        help_text="Candidate's last name",
    )
    first_name = models.CharField(
        verbose_name="first name",
        max_length=45,
        null=False,
        blank=True,
        help_text="Candidate's first name",
    )
    middle_name = models.CharField(
        verbose_name="middle name",
        max_length=20,
        null=False,
        blank=True,
        help_text="Candidate's middle name",
    )
    name_suffix = models.CharField(
        verbose_name="name suffix",
        max_length=10,
        null=False,
        blank=True,
        help_text="Candidate's name suffix",
    )
    f501_filing_id = models.IntegerField(
        verbose_name="f501 filing id",
        db_index=True,
        null=False,
        help_text="Candidate's Form 501 filing identification number",
    )
    last_f501_amend_id = models.IntegerField(
        verbose_name="last f501 amendment id",
        db_index=True,
        null=False,
        help_text="Most recent amendment number to the candidate's Form 501",
    )
    # mostly numeric only values, but a few with leading 0
    controlled_committee_filer_id = models.CharField(
        verbose_name="controlled committee identification number",
        max_length=9,
        null=False,
        blank=True,
        # need to double check all of these are actually filer ids
        help_text="Candidate's controlled committee filer identification number",
    )
    office = models.CharField(
        max_length=80,
        verbose_name='office sought',
        null=False,
        blank=True,
        help_text='Office sought by candidate',
    )
    district = models.CharField(
        max_length=4,
        verbose_name='district',
        null=False,
        blank=True,
        help_text='District of office sought (if applicable)',
    )
    agency = models.CharField(
        max_length=200,
        verbose_name='agency sought',
        null=False,
        blank=True,
        help_text='Agency of office sought',
    )
    jurisdiction = models.CharField(
        max_length=30,
        verbose_name='jurisdiction',
        null=False,
        blank=True,
        default='',
        help_text='Jurisdiction (e.g., "LOCAL", "STATE") of the office sought',
    )
    party = models.CharField(
        max_length=200,
        verbose_name='party',
        null=False,
        blank=True,
        help_text="Candidate's political party",
    )
    election_year = models.IntegerField(
        verbose_name='year of election',
        db_index=True,
        null=True,
        help_text='Year of election',
    )
    city = models.CharField(
        max_length=200,
        verbose_name='city',
        null=False,
        blank=True,
        help_text="Candidate's city",
    )
    state = models.CharField(
        max_length=200,
        verbose_name='state',
        null=False,
        blank=True,
        help_text="Candidate's state",
    )
    zip_code = models.CharField(
        max_length=10,
        verbose_name='zip code',
        null=False,
        blank=True,
        help_text="Candidate's zip code",
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='phone number',
        null=False,
        blank=True,
        help_text="Candidate's phone number",
    )
    fax = models.CharField(
        max_length=20,
        verbose_name='fax number',
        null=False,
        blank=True,
        help_text="Candidate's fax number",
    )
    email = models.CharField(
        max_length=200,
        verbose_name='email address',
        null=False,
        blank=True,
        help_text="Candidate's email address",
    )

    objects = ProcessedDataManager()

    class Meta:
        """
        Meta model options.
        """
        app_label = 'calaccess_processed'

    def __str__(self):
        return '{} {}'.format(
            self.first_name,
            self.last_name
        )


@python_2_unicode_compatible
class CandidateCommittee(models.Model):
    """
    Maps links between candidates and recipient committees.

    Derived from FILER_LINKS_CD.
    """
    candidate_filer_id = models.IntegerField(
        verbose_name='candidate filer ID',
        null=False,
        help_text="Unique filer_id of the candidate. Derived from FILER_ID_A "
                  "and FILER_ID_B columns on FILER_LINKS_CD, includes any "
                  "filer_id ever categorized as a candidate in "
                  "FILER_TO_FILER_TYPES_CD.",
    )
    committee_filer_id = models.IntegerField(
        verbose_name='committee filer ID',
        null=False,
        help_text="Unique filer_id of the committee linked to the candidate. "
                  "Derived from FILER_ID_A and FILER_ID_B columns on "
                  "FILER_LINKS_CD, includes any filer_id ever categorized as a"
                  " recipient committee that is linked to a filer_id "
                  "categorized as a candidate in FILER_TO_FILER_TYPES_CD.",
    )
    link_type_id = models.IntegerField(
        verbose_name='link type identifier',
        null=False,
        help_text="Numeric identifier that describes how the candidate and "
                  "committee are linked (the absolute value of FILER_LINKS_CD."
                  "LINK_TYPE).",
    )
    link_type_description = models.CharField(
        verbose_name='link type description',
        max_length=100,
        blank=False,
        null=False,
        help_text="Human-readable description of the link between the candidate"
                  " and committee (from LOOKUP_CODES_CD.CODE_DESC).",
    )
    first_session = models.IntegerField(
        verbose_name='first session',
        null=True,
        help_text="First session when the link between the candidate and "
                  "commitee existed (minimum value of "
                  "FILER_LINKS_CD.SESSION_ID).",
    )
    last_session = models.IntegerField(
        verbose_name='last session',
        null=True,
        help_text="Last session when the link between the candidate and "
                  "commitee existed (maximum value of "
                  "FILER_LINKS_CD.SESSION_ID).",
    )
    first_effective_date = models.DateField(
        verbose_name='first effective date',
        null=False,
        help_text="Earliest date when the link between the candidate and "
                  "commitee was in effect (minimum value of "
                  "FILER_LINKS_CD.EFFECTIVE_DATE).",
    )
    last_effective_date = models.DateField(
        verbose_name='last effective date',
        null=False,
        help_text="Latest date when the link between the candidate and "
                  "commitee was in effect (maximum value of "
                  "FILER_LINKS_CD.EFFECTIVE_DATE).",
    )
    first_termination_date = models.DateField(
        verbose_name='first termination date',
        null=True,
        help_text="Earliest date when the link between the candidate and "
                  "commitee was terminated (minimum value of "
                  "FILER_LINKS_CD.TERMINATION_DATE).",
    )
    last_termination_date = models.DateField(
        verbose_name='last termination date',
        null=True,
        help_text="Latest date when the link between the candidate and "
                  "commitee was terminated (minimum value of "
                  "FILER_LINKS_CD.TERMINATION_DATE).",
    )

    objects = ProcessedDataManager()

    class Meta:
        """
        Meta model options.
        """
        app_label = 'calaccess_processed'
        unique_together = ((
            'candidate_filer_id',
            'committee_filer_id',
            'link_type_id'
        ),)

    def __str__(self):
        return str(self.committee_filer_id)
