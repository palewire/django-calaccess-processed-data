#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing information scraped from the CAL-ACCESS website.
"""
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.opencivicdata.division import Division
from calaccess_processed.models.opencivicdata.people_orgs import (
    Organization,
    Person,
    Post,
)
import re


class BaseScrapedModel(models.Model):
    """
    Abstract base model from which all scraped models inherit.
    """
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Model options.
        """
        abstract = True


class BaseScrapedElection(BaseScrapedModel):
    """
    An election day scraped from the California Secretary of State's site.

    This is an abstract base model that creates two tables, one for elections
    scraped as part of the candidates scraper, and one for elections scraped
    as part of the propositions scraper.
    """
    name = models.CharField(
        max_length=200
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class CandidateScrapedElection(BaseScrapedElection):
    """
    An election day scraped as part of the `scrapecalaccesscandidates` command.
    """
    scraped_id = models.CharField(
        verbose_name="election identification number",
        max_length=3,
        blank=True,
    )
    sort_index = models.IntegerField(
        null=True,
        help_text="The index value is used to preserve sorting of elections, "
                  "since multiple elections may occur in a year. A greater sort "
                  "index corresponds to a more recent election."
    )

    def __str__(self):
        return self.name


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


@python_2_unicode_compatible
class PropositionScrapedElection(BaseScrapedElection):
    """
    An election day scraped as part of the `scrapecalaccesspropositions` command.
    """
    def __str__(self):
        return self.name

    def get_or_create_election(self):
        """
        Get or create an OCD Election object using the PropositionScrapedElection name.

        Returns a tuple (Election object, created), where created is a boolean
        specifying whether a Election was created.
        """
        from calaccess_processed.models.opencivicdata.elections import Election
        
        prop_name_pattern = r'^(?P<date>^[A-Z]+\s\d{1,2},\s\d{4})\s(?P<name>.+)$'
        # extract the name and date
        match = re.match(prop_name_pattern, self.name)
        dt_obj = timezone.make_aware(
            timezone.datetime.strptime(
                match.groupdict()['date'],
                '%B %d, %Y',
            )
        )
        name = '{0} {1}'.format(
            dt_obj.year,
            match.groupdict()['name'],
        ).upper()
        # try getting an existing OCD election with the same date
        created = False
        try:
            elec = Election.objects.get(start_time=dt_obj)
        except Election.DoesNotExist:
            # or make a new one
            elec = Election.objects.create(start_time=dt_obj, name=name)
        else:
            created = True
            # if election already exists and is named 'SPECIAL' or 'RECALL'
            if (
                'SPECIAL' in elec.name.upper() or
                'RECALL' in elec.name.upper()
            ):
                # and the matched election's name includes either 'GENERAL'
                # or 'PRIMARY'...
                if (
                    re.match(r'^\d{4} GENERAL$', name) or
                    re.match(r'^\d{4} PRIMARY$', name)
                ):
                    # update the name
                    elec.name = name
                    elec.save()
        return (elec, created)


@python_2_unicode_compatible
class ScrapedProposition(BaseScrapedModel):
    """
    A yes or no ballot measure for voters scraped from the California Secretary of State's site.
    """
    # Most of the time, this is a number, however,
    # it can be a bona fide name, e.g.
    # '2003 Recall Question'
    name = models.CharField(
        verbose_name="proposition name",
        max_length=200
    )
    scraped_id = models.CharField(
        verbose_name="proposition identification number",
        max_length=200
    )
    election = models.ForeignKey('PropositionScrapedElection', null=True)

    class Meta:
        """
        Model options.
        """
        ordering = ("-election", "name")

    def __str__(self):
        return 'Proposition: {}'.format(self.name)


class BaseScrapedCommittee(BaseScrapedModel):
    """
    An committee scraped from the California Secretary of State's site.

    This is an abstract base model that creates two tables, one for committees
    scraped as part of the candidates scraper, and one for committees scraped
    as part of the propositions scraper.
    """
    name = models.CharField(
        verbose_name="committee name",
        max_length=500
    )
    scraped_id = models.CharField(
        verbose_name="committee identification number",
        max_length=7
    )

    class Meta:
        """
        Model options.
        """
        abstract = True


@python_2_unicode_compatible
class ScrapedPropositionCommittee(BaseScrapedCommittee):
    """
    A committee supporting or opposing a proposition scraped from the California Secretary of State's site.
    """
    position = models.CharField(
        max_length=100,
        help_text="Whether the committee supports or opposes the proposition",
    )
    proposition = models.ForeignKey('ScrapedProposition')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ScrapedCandidateCommittee(BaseScrapedCommittee):
    """
    A candidate committee scraped from the California Secretary of State's site.
    """
    candidate_id = models.CharField(
        max_length=100
    )
    status = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name
