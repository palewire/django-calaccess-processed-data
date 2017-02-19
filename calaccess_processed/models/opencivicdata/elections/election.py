#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OCD Election-related models.
"""
from __future__ import unicode_literals
import warnings
from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from calaccess_processed.models.opencivicdata.base import IdentifierBase
from calaccess_processed.models.opencivicdata.event import Event
from calaccess_processed.models.opencivicdata.people_orgs import Organization
from calaccess_processed.models.scraper import (
    CandidateScrapedElection,
    PropositionScrapedElection,
)


class ElectionManager(models.Manager):
    """
    Manager with custom methods for OCD Election.
    """
    def create(self, start_time, name, **kwargs):
        """
        Custom create method for Election objects.
        """
        elex_div = Organization.objects.get(name='Elections Division')
        return super(
            ElectionManager,
            self,
        ).create(
            start_time=start_time,
            name=name,
            state='st06',
            all_day=True,
            timezone='US/Pacific',
            classification='election',
            administrative_org=elex_div,
            **kwargs
        )

    def load_raw_data(self):
        """
        Load Election model from CandidateScrapedElection and PropositionScrapedElection.
        """
        # start by loading the prop elections, which include a date in the name
        for p in PropositionScrapedElection.objects.all():
            p.get_or_create_election()

        # the "2008 PRIMARY" on 2/5/2008 is the presidential primary
        # plus some other special elections and propositions
        try:
            feb_08_primary = self.get(name='2008 PRIMARY', start_time__month=2)
        except Election.DoesNotExist:
            warnings.warn('Feb 2008 presidential primary election not found.')
        else:
            feb_08_primary.name = '2008 PRESIDENTIAL PRIMARY AND SPECIAL ELECTIONS'
            feb_08_primary.save()

        # this list is compiled from the candidate elections scraped from CAL-ACCESS:
        # http://cal-access.ss.ca.gov/Campaign/Candidates/
        # and also the SoS site:
        # http://www.sos.ca.gov/elections/prior-elections/special-elections/
        # http://elections.cdn.sos.ca.gov/special-elections/pdf/special-elections-history.pdf
        cand_elections_w_dates = (
            ('2016 SPECIAL ELECTION (ASSEMBLY 31)', '2016-4-5'),
            ('2015 SPECIAL RUNOFF (STATE SENATE 07)', '2015-5-19'),
            ('2015 SPECIAL ELECTION (STATE SENATE 07)', '2015-3-17'),
            ('2015 SPECIAL ELECTION (STATE SENATE 21)', '2015-3-17'),
            ('2015 SPECIAL ELECTION (STATE SENATE 37)', '2015-3-17'),
            ('2014 SPECIAL ELECTION (STATE SENATE 35)', '2014-12-9'),
            ('2014 SPECIAL ELECTION (STATE SENATE 23)', '2014-3-25'),
            ('2013 SPECIAL ELECTION (ASSEMBLY 54)', '2013-12-3'),
            ('2013 SPECIAL RUNOFF (ASSEMBLY 45)', '2013-11-19'),
            ('2013 SPECIAL ELECTION (ASSEMBLY 45)', '2013-9-17'),
            ('2013 SPECIAL RUNOFF (ASSEMBLY 52)', '2013-9-24'),
            ('2013 SPECIAL ELECTION (ASSEMBLY 52)', '2013-7-23'),
            ('2013 SPECIAL ELECTION (STATE SENATE 26)', '2013-9-17'),
            ('2013 SPECIAL RUNOFF (STATE SENATE 16)', '2013-7-23'),
            ('2013 SPECIAL ELECTION (STATE SENATE 16)', '2013-5-21'),
            ('2013 SPECIAL ELECTION (ASSEMBLY 80)', '2013-5-21'),
            ('2013 SPECIAL RUNOFF (STATE SENATE 32)', '2013-5-14'),
            ('2013 SPECIAL ELECTION (STATE SENATE 32)', '2013-3-12'),
            ('2013 SPECIAL ELECTION (STATE SENATE 40)', '2013-3-12'),
            ('2013 SPECIAL ELECTION (STATE SENATE 04)', '2013-1-8'),
            ('2012 SPECIAL ELECTION (STATE SENATE 04)', '2012-11-6'),
            ('2011 SPECIAL RUNOFF (ASSEMBLY 04)', '2011-5-3'),
            ('2011 SPECIAL ELECTION (ASSEMBLY 04)', '2011-3-8'),
            ('2011 SPECIAL ELECTION (STATE SENATE 28)', '2011-2-15'),
            ('2011 SPECIAL ELECTION (STATE SENATE 17)', '2011-2-15'),
            ('2011 SPECIAL RUNOFF (STATE SENATE 01)', '2011-1-4'),
            ('2010 SPECIAL ELECTION (STATE SENATE 01)', '2010-11-2'),
            ('2010 SPECIAL RUNOFF (STATE SENATE 15)', '2010-8-17'),
            ('2010 SPECIAL ELECTION (STATE SENATE 15)', '2010-6-22'),
            ('2010 SPECIAL RUNOFF (STATE SENATE 37)', '2010-6-8'),
            ('2010 SPECIAL ELECTION (STATE SENATE 37)', '2010-4-13'),
            ('2010 SPECIAL RUNOFF (ASSEMBLY 43)', '2010-6-8'),
            ('2010 SPECIAL ELECTION (ASSEMBLY 43)', '2010-4-13'),
            ('2010 SPECIAL RUNOFF (ASSEMBLY 72)', '2010-1-12'),
            ('2009 SPECIAL ELECTION (ASSEMBLY 72)', '2009-11-17'),
            ('2009 SPECIAL ELECTION (ASSEMBLY 51)', '2009-9-1'),
            ('2009 SPECIAL RUNOFF (STATE SENATE 26)', '2009-5-19'),
            ('2009 SPECIAL ELECTION (STATE SENATE 26)', '2009-3-24'),
            ('2008 SPECIAL RUNOFF (ASSEMBLY 55)', '2008-2-5'),
            ('2007 SPECIAL ELECTION (ASSEMBLY 55)', '2007-12-11'),
            ('2007 SPECIAL ELECTION (ASSEMBLY 39)', '2007-5-15'),
            ('2006 SPECIAL RUNOFF (STATE SENATE 35)', '2006-6-6'),
            ('2006 SPECIAL ELECTION (STATE SENATE 35)', '2006-4-11'),
            ('2005 SPECIAL ELECTION (ASSEMBLY 53)', '2005-9-13'),
            ('2003 SPECIAL ELECTION (GOVERNOR)', '2003-10-7'),
            ('2001 SPECIAL ELECTION (ASSEMBLY 49)', '2001-5-15'),
            ('2001 SPECIAL RUNOFF (ASSEMBLY 65)', '2001-2-6'),
            ('2001 SPECIAL ELECTION (ASSEMBLY 65)', '2001-4-3'),
            ('2001 SPECIAL ELECTION (STATE SENATE 24)', '2001-3-26'),
        )

        # then loop over the candidate elections
        for c in CandidateScrapedElection.objects.all():
            # skip if the candidate election id is already linked to an OCD election
            e_id = ElectionIdentifier.objects.filter(
                scheme='calaccess_election_id',
                identifier=c.scraped_id
            )
            if e_id.exists():
                elec = e_id[0].election
                elec.sources.update_or_create(
                    url=c.url,
                    note='Last scraped on {dt:%Y-%m-%d}'.format(
                        dt=c.last_modified,
                    )
                )
            else:
                # if the name is in the list of special elections
                if c.name in (x[0] for x in cand_elections_w_dates):
                    date = dict(cand_elections_w_dates)[c.name]
                    dt_obj = timezone.make_aware(
                        timezone.datetime.strptime(
                            date,
                            '%Y-%m-%d',
                        )
                    )
                    # get or create the special election
                    try:
                        elec = self.get(start_time=dt_obj)
                    except self.model.DoesNotExist:
                        elec = self.create(
                            start_time=dt_obj,
                            name=c.name,
                            is_statewide=False,
                        )
                else:
                    # assume the candidate election name is in the
                    # '{year} {type}' format
                    try:
                        elec = self.get(name=c.name)
                    except Election.DoesNotExist:
                        # this recall election occurred on the same date as 2008 primary
                        # http://www.sos.ca.gov/elections/prior-elections/special-elections/special-recall-election-senate-district-12-june-3-2008/
                        # http://www.sos.ca.gov/elections/prior-elections/statewide-election-results/statewide-direct-primary-election-june-3-2008/
                        if c.name == '2008 RECALL (STATE SENATE 12)':
                            elec = self.get(name='2008 PRIMARY')
                        else:
                            raise Exception('Missing record for %s' % c.name)

                elec.identifiers.create(
                    scheme='calaccess_election_id',
                    identifier=c.scraped_id
                )
                elec.sources.update_or_create(
                    url=c.url,
                    note='Last scraped on {dt:%Y-%m-%d}'.format(
                        dt=c.last_modified,
                    )
                )

        # Remove office from name of special elections with multiple races
        special_elections = self.filter(
            name__regex=r'^\d{4}\sSPECIAL\s.+\(.+$'
        ).annotate(
            num_ids=Count('identifiers')
        ).filter(num_ids__gte=2)

        for se in special_elections:
            se.name = '{0} SPECIAL ELECTIONS'.format(
                se.start_time.strftime('%b %Y').upper()
            )
            se.save()

        return


@python_2_unicode_compatible
class Election(Event):
    """
    OCD Election model.
    """
    objects = ElectionManager()

    administrative_org = models.ForeignKey(
        'Organization',
        related_name='elections',
        null=True,
        help_text='Reference to the OCD ``Organization`` that administers the election.',
    )
    state = models.CharField(
        max_length=4,
        help_text='FIPS code of the state where the election is being held. '
                  'Recorded in the format ``st{{fips}}`` to match references '
                  'to VIP elements.',
    )
    is_statewide = models.BooleanField(
        default=True,
        help_text='Indicates whether the election is statewide.',
    )

    class Meta(Event.Meta):
        """
        Model options.
        """
        ordering = ("-start_time",)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ElectionIdentifier(IdentifierBase):
    """
    Model for storing an OCD Election's other identifiers.
    """
    election = models.ForeignKey(
        Election,
        related_name='identifiers'
    )

    def __str__(self):
        tmpl = '%s identifies %s'
        return tmpl % (self.identifier, self.election)
