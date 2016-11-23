#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing propositions derived from scraped CAL-ACCESS data.
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
    propositions = models.ManyToManyField(
        'Proposition',
        through='PropositionSupportOppose',
        help_text="Propositions supported or opposed by this committee",
        related_name='committees'
    )

    objects = ProcessedDataManager()

    @property
    def supports(self):
        """
        Propositions supported by this committee"
        """
        return self.propositions.filter(
            propositionsupportoppose__support_oppose='S'
        )

    @property
    def opposes(self):
        """
        Propositions opposed by this committee"
        """
        return self.propositions.filter(
            propositionsupportoppose__support_oppose='O'
        )

    def __str__(self):
        return self.name


class PropositionSupportOppose(models.Model):
    """
    Stores information about committees and the propositions
    that they support or oppose.
    """
    committee = models.ForeignKey(
        'PropositionCommittee',
        on_delete=models.CASCADE,
        help_text='Committee that supports or opposes the proposition'
    )
    proposition = models.ForeignKey(
        'Proposition',
        on_delete=models.CASCADE,
        help_text='Proposition supported or opposed by the committee'
    )
    SUPPORT_OPPOSE_CHOICES = (
        ('S', 'Support'),
        ('O', 'Oppose')
    )
    support_oppose = models.CharField(
        verbose_name="support or oppose",
        max_length=1,
        null=False,
        blank=True,
        choices=SUPPORT_OPPOSE_CHOICES,
        help_text="Whether the committee supports or opposes the proposition",
    )
