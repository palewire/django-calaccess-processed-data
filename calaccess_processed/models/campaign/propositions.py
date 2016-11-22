#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing propositions derived from raw CAL-ACCESS data.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.managers import ProcessedDataManager


@python_2_unicode_compatible
class Proposition(models.Model):
    """
    A single proposition on the California ballot.

    Scraped from the CAL-ACCESS site.
    """
    id = models.IntegerField(
        primary_key=True,
        verbose_name="proposition ID",
        null=False,
        help_text="Proposition unique id cast as an integer.",
        unique=True
    )
    name = models.CharField(
        verbose_name="name",
        max_length=500,
        null=False,
        blank=True,
        help_text="Name of the proposition",
    )
    election = models.ForeignKey(
        'Election',
        related_name='election',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Foreign key referring to the election in which this'
                  'proposition was on the ballot'
    )

    objects = ProcessedDataManager()

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class PropositionCommittee(models.Model):
    """
    A committee that supports or opposes at least one proposition.

    Scraped from the CAL-ACCESS site.
    """
    id = models.IntegerField(
        primary_key=True,
        verbose_name="committee ID",
        null=False,
        help_text="Committee unique id cast as an integer.",
        unique=True
    )
    name = models.CharField(
        verbose_name="name",
        max_length=500,
        null=False,
        blank=True,
        help_text="Name of the proposition",
    )
    supports = models.ManyToManyField(
        'Proposition',
        related_name='supporting_committees',
        help_text="Propositions supported by this committee",
    )
    opposes = models.ManyToManyField(
        'Proposition',
        related_name='opposing_committees',
        help_text="Propositions opposed by this committee",
    )

    objects = ProcessedDataManager()

    def __str__(self):
        return self.name
