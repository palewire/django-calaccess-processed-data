#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
import re
import logging
from calaccess_processed import corrections
from django.db.models.functions import Concat
from django.db.models import Value, CharField
from ..opencivicdata.candidacies import OCDCandidacyProxy
from ..opencivicdata.posts import OCDPostProxy
from ..opencivicdata.parties import OCDPartyProxy
from .candidateelections import ScrapedCandidateElectionProxy
from calaccess_scraped.models import Candidate, Incumbent
from opencivicdata.elections.models import CandidateContest
logger = logging.getLogger(__name__)
corrections


class ScrapedNameMixin(object):
    """
    Tools for cleaning up scraped candidate names.
    """
    @property
    def corrected_name(self):
        """
        Returns the scraped name with any corrections made.
        """
        fixes = {
            # http://www.sos.ca.gov/elections/prior-elections/statewide-election-results/primary-election-march-7-2000/certified-list-candidates/ # noqa
            'COURTRIGHT DONNA': 'COURTRIGHT, DONNA'
        }
        return fixes.get(self.name, self.name)

    @property
    def parsed_name(self):
        """
        Return a dict of formatted Person name field values.
        """
        # sort_name is undoctored name from scrape
        d = {
            'sort_name': self.name.strip()
        }

        # parse out these suffixes: JR, SR, II, III
        suffix_pattern = r'(?:^|\s)((?:[JS]R\.?)|(?:I{2,3}))(?:,|\s|$)'
        match = re.search(suffix_pattern, d['sort_name'])
        if match:
            # replace suffix with a comma
            # and replace any double commas, strip any trailing
            d['sort_name'] = d['sort_name'].replace(match.group(), ',').replace(',,', ',')
            d['sort_name'] = re.sub(r',\s?$', '', d['sort_name']).strip()

        # split once, strip and flip the sort_name to make name
        split_name = [i.strip() for i in d['sort_name'].split(',', 1)]
        name_list = list(split_name)
        name_list.reverse()
        d['name'] = ' '.join(name_list).strip()
        d['family_name'] = split_name[0]
        if len(split_name) > 1:
            d['given_name'] = split_name[1]
        if match:
            # append suffix to end of name and given_name
            suffix = ' %s' % match.group().replace(',', '').strip()
            d['name'] += suffix
            if 'given_name' in d:
                d['given_name'] += suffix

        return d

    def parse_office_name(self):
        """
        Parse string containg the name for an office.

        Expected format is "{TYPE NAME} [{DISTRICT NUMBER}]".

        Return a dict with two keys: type and district.
        """
        office_pattern = r'^(?P<type>[A-Z ]+)(?P<district>\d{2})?$'
        try:
            parsed = re.match(office_pattern, self.office_name.upper()).groupdict()
        except AttributeError:
            parsed = {'type': None, 'district': None}
        else:
            parsed['type'] = parsed['type'].strip()
            try:
                parsed['district'] = int(parsed['district'])
            except TypeError:
                pass
        return parsed


class ScrapedIncumbentProxy(Incumbent, ScrapedNameMixin):
    """
    A proxy for the calaccess_scraped Incumbent model.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True
        ordering = ['-session']


class ScrapedCandidateProxy(Candidate, ScrapedNameMixin):
    """
    A proxy for the calaccess_scraped Candidate model.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True

    @property
    def election_proxy(self):
        """
        Return the proxy model for the related election object.
        """
        return ScrapedCandidateElectionProxy.objects.get(id=self.election.id)

    @property
    def post_proxy(self):
        """
        Return the proxy model for the related post object.
        """
        post, post_created = OCDPostProxy.objects.get_or_create_by_name(
            self.office_name
        )
        return post

    def get_corrected_party(self):
        """
        Returns a manually correction to the candidate's party, if it's been made. Otherwise returns None.
        """
        scraped_election = self.election_proxy
        return corrections.candidate_party(
            self.name,
            scraped_election.date.year,
            scraped_election.election_type,
            self.office_name,
        )

    def get_party(self):
        """
        Returns the party we believe the candidate was associated with this election.
        """
        # First, if the candidate is running for this office, it is by definition non-partisan
        if self.office_name == 'SUPERINTENDENT OF PUBLIC INSTRUCTION':
            logger.debug("{} party set to NO PARTY PREFERENCE based on office".format(self))
            return OCDPartyProxy.objects.get(name="NO PARTY PREFERENCE")

        # Next pull the OCD election record so we have it to inspect
        scraped_election = self.election_proxy

        # Check if this candidate has been manually corrected.
        party = self.get_corrected_party()
        # If so, just pass that out right away
        if party:
            logger.debug("{} party set to {} based on correction".format(self, party))
            return party

        # Next, if they have filed a 501 form, let's use that
        form501 = self.get_form501_filing()
        if form501:
            # Try getting party from form 501 party
            party = OCDPartyProxy.objects.get_by_name(form501.party)
            if not party.is_unknown():
                logger.debug("{} party set to {} based on Form 501 party".format(self, party))
                return party

            # Try getting it from form 501 filer id
            party = OCDPartyProxy.objects.get_by_filer_id(int(form501.filer_id), scraped_election.date)
            if not party.is_unknown():
                logger.debug("{} party set to {} based on Form 501 filer id".format(self, party))
                return party

        # If there's no 501, or if the 501 returned an unknown party ...
        # ... try one last stab at using the filer id (assuming it exists)
        if self.scraped_id:
            party = OCDPartyProxy.objects.get_by_filer_id(int(self.scraped_id), scraped_election.date)
            logger.debug("{} party set to {} after checking its scraped filer id".format(self, party))
            return party
        # Otherwise just give up and return the unknown party
        else:
            logger.debug("{} party set to UNKNOWN after failing to find a match".format(self))
            return OCDPartyProxy.objects.get(name="UNKNOWN")

    def get_form501_filing(self):
        """
        Return a Form501Filing that matches the scraped Candidate.

        By default, return the latest Form501FilingVersion, unless earliest
        is set to True.

        If the scraped Candidate has a scraped_id, lookup the Form501Filing
        by filer_id. Otherwise, lookup using the candidate's name.

        Return None can't match to a single Form501Filing.
        """
        from calaccess_processed.models import Form501Filing

        election_data = self.election_proxy.parsed_name
        office_data = self.parse_office_name()

        # filter all form501 lookups by office type, district and election year
        # get the most recently filed Form501 within the election_year
        q = Form501Filing.objects.filter(
            office__iexact=office_data['type'],
            district=office_data['district'],
            election_year__lte=election_data['year'],
        )

        if self.scraped_id != '':
            try:
                # first, try to get w/ filer_id and election_type
                form501 = q.filter(
                    filer_id=self.scraped_id,
                    election_type=election_data['type']
                ).latest('date_filed')
            except Form501Filing.DoesNotExist:
                # if that fails, try dropping election_type from filter
                try:
                    form501 = q.filter(filer_id=self.scraped_id).latest('date_filed')
                except Form501Filing.DoesNotExist:
                    form501 = None
        else:
            # if no filer_id, combine name fields from form501
            # first try "<last_name>, <first_name>" format.
            q = q.annotate(
                full_name=Concat(
                    'last_name',
                    Value(', '),
                    'first_name',
                    output_field=CharField(),
                )
            )
            # check if there are any with the "<last_name>, <first_name>"
            if not q.filter(full_name=self.name).exists():
                # use "<last_name>, <first_name> <middle_name>" format
                q = q.annotate(
                    full_name=Concat(
                        'last_name',
                        Value(', '),
                        'first_name',
                        Value(' '),
                        'middle_name',
                        output_field=CharField(),
                    ),
                )

            try:
                # first, try to get w/ filer_id and election_type
                form501 = q.filter(
                    full_name=self.name,
                    election_type=election_data['type'],
                ).latest('date_filed')
            except Form501Filing.DoesNotExist:
                # if that fails, try dropping election_type from filter
                try:
                    form501 = q.filter(full_name=self.name).latest('date_filed')
                except Form501Filing.DoesNotExist:
                    form501 = None

        return form501

    def get_or_create_contest(self):
        """
        Get or create an OCD CandidateContest object.

        Returns a tuple (CandidateContest object, created), where created is a boolean
        specifying whether a CandidateContest was created.
        """
        # Get election data
        scraped_election = self.election_proxy

        # Get the candidate's party
        candidate_party = self.get_party()

        # Assume all "SPECIAL" candidate elections are for contests where the
        # previous term of the office was unexpired.
        if scraped_election.is_special:
            previous_term_unexpired = True
            # We are not setting a contest party here for the reasons laid out in the following ticket:
            # https://github.com/california-civic-data-coalition/django-calaccess-processed-data/issues/70#issuecomment-300836502  # NOQA
            contest_party = None
            contest_name = '{} ({})'.format(self.office_name, scraped_election.election_type)
        # Otherwise, we assume this a typical election
        else:
            # At a minimum, that means that the previous term has expired for the office
            previous_term_unexpired = False
            # Beyond that, there are two different cases depending on when the election was held.
            # Prior to 2012, California held partisan primaries. Since then, the state has held
            # open "jungle" primaries that set all candidates for the same office against each other,
            # regardless of their party.
            # In the case of partisan elections, we want to make sure the candidates are separated by party.
            # The one exception to this is superintendent races which have always been non-partisan.
            if scraped_election.is_partisan_primary and self.office_name != 'SUPERINTENDENT OF PUBLIC INSTRUCTION':
                # In this case, the contest party should be the same as the candidate party.
                contest_party = candidate_party
                # If the party is unknown, just tack party on the end of the contest name
                if candidate_party.is_unknown():
                    contest_name = '{} ({} PARTY)'.format(self.office_name, candidate_party.name)
                # For a regular party, we shouldn't have to do much here.
                else:
                    contest_name = '{} ({})'.format(self.office_name, candidate_party.name)
            # If this is a general election prior to 2012, or any non-special election since then ...
            else:
                # ... there is no party for the contest ...
                contest_party = None
                # ... and there's no need to do anything to the contest name.
                contest_name = self.office_name

        # Make it happen
        contest, created = CandidateContest.objects.get_or_create(
            election=scraped_election.get_ocd_election(),
            name=contest_name,
            previous_term_unexpired=previous_term_unexpired,
            party=contest_party,
            division=self.post_proxy.division,
        )

        # if contest was created, add the Post
        if created:
            contest.posts.create(post=self.post_proxy)

        # Always update the source for the contest
        contest.sources.update_or_create(
            url=self.url,
            note='Last scraped on {dt:%Y-%m-%d}'.format(dt=self.last_modified)
        )

        # Return the contest and whether or not it was created
        return contest, created

    def get_loaded_ocd_candidacy(self):
        """
        Get and OCD candidacy previously loaded from the scraped Candidate.

        First, try getting a Candidacy using the election, post and filer_id. Then,
        try election, post and name (candidate_name, person.name or
        person__other_name__name).
        """
        scraped_election = self.election_proxy
        ocd_election = scraped_election.get_ocd_election()

        q = OCDCandidacyProxy.objects.filter(
            contest__election=ocd_election,
            post=self.post_proxy,
        )
        if self.scraped_id:
            try:
                candidacy = q.get_by_filer_id(self.scraped_id)
            except OCDCandidacyProxy.MultipleObjectsReturned:
                # distinguish between special and regular elections that
                # happen on the same day
                if scraped_election.is_special:
                    q = q.filter(
                        contest__name__icontains=scraped_election.election_type
                    )
                else:
                    q = q.exclude(
                        contest__name__icontains='SPECIAL'
                    )
                candidacy = q.get_by_filer_id(self.scraped_id)
        else:
            try:
                candidacy = q.get_by_name(self.parsed_name['name'])
            except OCDCandidacyProxy.MultipleObjectsReturned:
                # distinguish between special and regular elections that
                # happen on the same day
                if scraped_election.is_special:
                    q = q.filter(
                        contest__name__icontains=scraped_election.election_type
                    )
                else:
                    q = q.exclude(
                        contest__name__icontains='SPECIAL'
                    )
                candidacy = q.get_by_name(self.parsed_name['name'])

        return candidacy
