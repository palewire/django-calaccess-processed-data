#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing candidate information scraped from the CAL-ACCESS website.
"""
from __future__ import unicode_literals
import re
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.scraper.base import BaseScrapedModel
from opencivicdata.models.division import Division
from opencivicdata.models.people_orgs import (
    Organization,
    Person,
    Post,
)


@python_2_unicode_compatible
class ScrapedCandidate(BaseScrapedModel):
    """
    A candidate for office scraped from the California Secretary of State's site.
    """
    name = models.CharField(
        verbose_name="candidate name",
        max_length=200
    )
    scraped_id = models.CharField(
        verbose_name="candidate identification number",
        max_length=7,
        blank=True,  # Some don't have IDs on the website
    )
    office_name = models.CharField(
        verbose_name="name of the office for which this candidate is running",
        max_length=100,
        blank=True
    )
    election = models.ForeignKey('CandidateScrapedElection', null=True)

    def __str__(self):
        return self.name

    def get_or_create_post(self):
        """
        Get or create a Post object using the ScrapedCandidate office_name.

        Returns a tuple (Post object, created), where created is a boolean
        specifying whether a Post was created.
        """
        office_pattern = r'^(?P<type>[A-Z ]+)(?P<dist>\d{2})?$'

        match = re.match(office_pattern, self.office_name.upper())
        office_type = match.groupdict()['type'].strip()
        try:
            district_num = int(match.groupdict()['dist'])
        except TypeError:
            pass

        # prepare to get or create post
        raw_post = {'label': self.office_name.title().replace('Of', 'of')}

        if office_type == 'STATE SENATE':
            raw_post['division'] = Division.objects.get(
                subtype2='sldu',
                subid2=str(district_num),
            )
            raw_post['organization'] = Organization.objects.get(
                classification='upper',
            )
            raw_post['role'] = 'Senator'
        elif office_type == 'ASSEMBLY':
            raw_post['division'] = Division.objects.get(
                subtype2='sldl',
                subid2=str(district_num),
            )
            raw_post['organization'] = Organization.objects.get(
                classification='lower',
            )
            raw_post['role'] = 'Assembly Member'
        else:
            raw_post['division'] = Division.objects.get(
                id='ocd-division/country:us/state:ca'
            )
            if office_type == 'MEMBER BOARD OF EQUALIZATION':
                raw_post['organization'] = Organization.objects.get(
                    name='State Board of Equalization',
                )
                raw_post['role'] = 'Board Member'
            elif office_type == 'SECRETARY OF STATE':
                raw_post['organization'] = Organization.objects.get(
                    name='California Secretary of State',
                )
                raw_post['role'] = raw_post['label']
            else:
                raw_post['organization'] = Organization.objects.get(
                    name='California State Executive Branch',
                )
                raw_post['role'] = raw_post['label']

        return Post.objects.get_or_create(**raw_post)

    def get_or_create_person(self):
        """
        Get or create a Person object using the ScrapedCandidate name and scraped_id.

        If a Person object is created and scraped_id is not blank, a PersonIdentifier
        object is also created.

        Returns a tuple (Person object, created), where created is a boolean
        specifying whether a Person was created.
        """
        person = Person.objects.get_using_filer_id(self.scraped_id)

        if not person:
            # split and flip the original name string
            split_name = self.name.split(',')
            split_name.reverse()
            person = Person.objects.create(
                sort_name=self.name,
                name=' '.join(split_name).strip()
            )
            if self.scraped_id != '':
                person.identifiers.create(
                    scheme='calaccess_filer_id',
                    identifier=self.scraped_id,
                )
            created = True
        else:
            created = False

        return (person, created)
