#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing campaign-related entities derived from raw CAL-ACCESS data.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.managers import ProcessedDataManager


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
        return str(self.full_name)


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

