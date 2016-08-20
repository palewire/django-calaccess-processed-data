#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing campaign finance tables derived from raw CAL-ACCESS data.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.managers import ProcessedDataManager


@python_2_unicode_compatible
class Candidate(models.Model):
    """
    Names, contact information and offices of person's running for elected office.
    """
    filer_id = models.IntegerField(
        verbose_name='filer ID',
        db_index=True,
        null=False,
        help_text="filer's unique identification number"
    )
    full_name = models.CharField(
        max_length=200,
        verbose_name='full name',
        null=False,
        help_text="Full name of candidate",
    )
    office = models.CharField(
        max_length=200,
        verbose_name='office sought',
        null=True,
        help_text='Office sought by candidate',
    )
    district = models.CharField(
        max_length=200,
        verbose_name='district',
        null=True,
        help_text='District of office sought (if applicable)',
    )
    agency = models.CharField(
        max_length=200,
        verbose_name='agency sought',
        null=True,
        help_text='Agency of office sought',
    )
    party = models.CharField(
        max_length=200,
        verbose_name='party',
        null=True,
        help_text="Candidate's political party",
    )
    election_year = models.IntegerField(
        verbose_name='year of election',
        null=True,
        help_text='Year of election',
    )
    city = models.CharField(
        max_length=200,
        verbose_name='city',
        null=True,
        help_text="Candidate's city",
    )
    state = models.CharField(
        max_length=200,
        verbose_name='state',
        null=True,
        help_text="Candidate's state",
    )
    zip_code = models.CharField(
        max_length=10,
        verbose_name='zip code',
        null=True,
        help_text="Candidate's zip code",
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='phone number',
        null=True,
        help_text="Candidate's phone number",
    )
    fax = models.CharField(
        max_length=20,
        verbose_name='fax number',
        null=True,
        help_text="Candidate's fax number",
    )
    email = models.CharField(
        max_length=200,
        verbose_name='email address',
        null=True,
        help_text="Candidate's email address",
    )

    objects = ProcessedDataManager()

    class Meta:
        """
        Meta model options.
        """
        app_label = 'calaccess_processed'
        ordering = ('filer_id', '-election_year',)

    def __str__(self):
        return str(self.full_name)
