#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy model for augmenting ScrapedCandidate model with methods useful for processing.
"""
from __future__ import unicode_literals
import logging
from calaccess_processed import corrections
from calaccess_scraped.models import Candidate
from django.db.models.functions import Concat
from django.db.models import Value, CharField
from opencivicdata.elections.models import CandidateContest
from .base import ScrapedNameMixin
from .candidateelections import ScrapedCandidateElectionProxy
from ..opencivicdata.candidacies import OCDCandidacyProxy
from ..opencivicdata.posts import OCDPostProxy
from ..opencivicdata.parties import OCDPartyProxy
logger = logging.getLogger(__name__)
corrections


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
        Returns the party we believe the candidate was associated with in this election.
        """
        from calaccess_processed.models import Form501Filing

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

        # Next, check if they have filed any Form 501s
        try:
            form501s = self.get_form501s()[0].order_by('-date_filed')
        except Form501Filing.DoesNotExist:
            pass
        else:
            for i in form501s.all():
                # Try getting party from form 501 party
                party = OCDPartyProxy.objects.get_by_name(i.party)
                if not party.is_unknown():
                    logger.debug(
                        "{} party set to {} based on Form 501 party".format(self, party)
                    )
                    return party
                # Try getting it from form 501 filer id
                party = OCDPartyProxy.objects.get_by_filer_id(int(i.filer_id), scraped_election.date)
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

    def match_form501s_by_scraped_id(self):
        """
        Get Form501Filings with filer_ids that match candidate's scraped_id.

        First, filter to matches with the same election_type and office where the
        election_year is the same or earlier than the scraped election's year.

        If none are found, search for matches with the same office office before
        where the election_year is the same or earlier than the election_year.

        Return a Form501Filing QuerySet.
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
            filer_id=self.scraped_id,
        )

        # filter to election_type if it will yield results
        if q.filter(election_type=election_data['type']).exists():
            q = q.filter(election_type=election_data['type'])

        return q

    def match_form501s_by_name(self):
        """
        Get Form501Filings with names that match the scraped candidate's name.

        Returns a Form501Filing QuerySet.
        """
        from calaccess_processed.models import Form501Filing

        election_data = self.election_proxy.parsed_name
        office_data = self.parse_office_name()

        q = Form501Filing.objects.filter(
            office__iexact=office_data['type'],
            district=office_data['district'],
            election_year__lte=election_data['year'],
        )
        # first, try "<last_name>, <first_name> <middle_name>" format
        last_first_middle_q = q.annotate(
            full_name=Concat(
                'last_name',
                Value(', '),
                'first_name',
                Value(' '),
                'middle_name',
                output_field=CharField(),
            ),
        ).filter(full_name=self.name)

        # limit scope to election_type if it will yield results
        if last_first_middle_q.filter(election_type=election_data['type']).exists():
            q = last_first_middle_q.filter(election_type=election_data['type'])
        # if not, check if dropping election_type filter yields results
        elif last_first_middle_q.exists():
            q = last_first_middle_q
        # if not, change name format
        else:
            last_first_q = q.annotate(
                full_name=Concat(
                    'last_name',
                    Value(', '),
                    'first_name',
                    output_field=CharField(),
                ),
            ).filter(full_name=self.name)

            # again, limit to election_type at first
            if last_first_q.filter(election_type=election_data['type']).exists():
                q = last_first_q.filter(election_type=election_data['type'])
            else:
                q = last_first_q

        return q

    def get_form501s(self):
        """
        Get the Form501Filings for the scraped candidate.

        If none, raise a Form501Filing.DoesNotExist exception.

        Return a tuple with Form501Filing QuerySet and str describing match criteria.
        """
        from calaccess_processed.models import Form501Filing

        if self.match_form501s_by_scraped_id().exists():
            return (self.match_form501s_by_scraped_id(), 'scraped_id')
        elif self.match_form501s_by_name().exists():
            return (self.match_form501s_by_name(), 'name')
        else:
            raise Form501Filing.DoesNotExist()

    def get_or_create_contest(self):
        """
        Get or create an OCD CandidateContest object.

        Primary contests before 2012 were each linked to a Party. Unless the user
        passes a value via the party keyword argument, the Party linked to the scraped
        candidate's most recent Form501Filing will be selected.

        Returns a tuple (CandidateContest object, created), where created is a boolean
        specifying whether a CandidateContest was created.
        """
        # Get election data
        scraped_election = self.election_proxy

        # Get the candidate's party
        candidate_party = self.get_party()

        # Assume all "SPECIAL" and "RECALL" candidate elections are for contests
        # where the previous term of the office was unexpired.
        if scraped_election.is_special or scraped_election.is_recall:
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
        Get an OCD candidacy previously loaded from the scraped Candidate.

        Matches are scoped to OCD Candidacies where:
        - The OCD Election linked to the scraped election's id
        - The Post that's equivalent to the scrape candidate's office_name
        - If the scraped election is "special", OCD CandidateContest where
        the previous term is unexpired.
        - If the scraped election is "regular", OCD CandidateContest where
        the previous term is expired.

        If the scraped candidate has a filer_id, use this in the matching
        criteria. Otherwise, match on candidate_name, person.name or
        person__other_name__name.

        Returns a Candidacy object.
        """
        scraped_election = self.election_proxy
        ocd_election = scraped_election.get_ocd_election()

        q = OCDCandidacyProxy.objects.filter(
            contest__election=ocd_election,
            post=self.post_proxy,
        )

        # for special elections, filter to contests with unexpired terms
        if scraped_election.is_special or scraped_election.is_recall:
            q = q.filter(contest__previous_term_unexpired=True)
        # for regular elections, filter to contests with expired_terms
        elif scraped_election.is_regular:
            q = q.filter(contest__previous_term_unexpired=False)
        else:
            raise Exception(
                'Unknown election type for %s.' % scraped_election
            )

        if self.scraped_id:
            candidacy = q.get_by_filer_id(self.scraped_id)
        else:
            candidacy = q.get_by_name(self.parsed_name['name'])

        return candidacy
