#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load OCD BallotMeasureContest and related models with data scraped from the CAL-ACCESS website.
"""
import re
from django.utils import timezone
from calaccess_processed.models import OCDElectionProxy
from calaccess_scraped.models import PropositionElection
from calaccess_processed.management.commands import CalAccessCommand
from opencivicdata.elections.models import OCDDivisionProxy, BallotMeasureContest


class Command(CalAccessCommand):
    """
    Load OCD BallotMeasureContest and related models with data scraped from the CAL-ACCESS website.
    """
    help = 'Load OCD BallotMeasureContest and related models with data scraped from the CAL-ACCESS website'
    header_log = 'Loading Ballot Measure Contests'

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.header(self.header_log)
        if options['flush']:
            self.flush()
        self.load()
        self.success("Done!")

    def get_scraped_elecs(self):
        """
        Get the scraped elections with propositions to load.

        Return QuerySet.
        """
        return PropositionElection.objects.all()

    def get_scraped_props(self, scraped_elec):
        """
        Get the scraped propositions within the scraped election to load.

        Return QuerySet.
        """
        # Recalls are being excluded so they can be loaded in a separate command.
        return scraped_elec.propositions.exclude(name__icontains='RECALL')

    def get_or_create_election(self, scraped_elec):
        """
        Get or create an OCD Election object using the scraped PropositionElection.

        Returns a tuple (Election object, created), where created is a boolean
        specifying whether a Election was created.
        """
        # Extract the name and date from the election name
        prop_name_pattern = r'^(?P<date>^[A-Z]+\s\d{1,2},\s\d{4})\s(?P<name>.+)$'
        match = re.match(prop_name_pattern, scraped_elec.name)

        # Convert it to a datetime object
        date_obj = timezone.datetime.strptime(
            match.groupdict()['date'],
            '%B %d, %Y',
        ).date()

        # Format that as a string
        name = '{0} {1}'.format(date_obj.year, match.groupdict()['name']).upper()

        # Differentiate between two '2008 PRIMARY' ballot measure elections
        if name == '2008 PRIMARY' and date_obj.month == 2:
            name = "2008 PRESIDENTIAL PRIMARY AND SPECIAL ELECTIONS"

        # Try getting an existing Election with the same date
        try:
            elec = OCDElectionProxy.objects.get(date=date_obj)
        except OCDElectionProxy.DoesNotExist:
            # or make a new one
            elec = OCDElectionProxy.objects.create_with_name_and_date(name, date_obj)
            created = True
        else:
            created = False
            # If election already exists and is named 'SPECIAL' or 'RECALL' ...
            if 'SPECIAL' in elec.name.upper() or 'RECALL' in elec.name.upper():
                # ... and the matched election's name includes either 'GENERAL' or 'PRIMARY'...
                if (
                    re.match(r'^\d{4} GENERAL$', name) or
                    re.match(r'^\d{4} PRIMARY$', name)
                ):
                    # Update the name, since it could change on the site
                    elec.name = name
                    elec.save()
        return (elec, created)

    def create_contest(self, scraped_prop, ocd_elec):
        """
        Create an OCD BallotMeasureContest object derived from a ScrapedProposition.

        Return a BallotMeasureContest object.
        """
        # Set the classification
        if 'REFERENDUM' in scraped_prop.name:
            classification = 'referendum'
        elif (
            'INITIATIVE' in scraped_prop.name or
            'INITATIVE' in scraped_prop.name
        ):
            classification = 'initiative'
        else:
            classification = 'ballot measure'

        # Create the object
        return BallotMeasureContest.objects.create(
            election=ocd_elec,
            division=OCDDivisionProxy.objects.california(),
            name=scraped_prop.name,
            classification=classification,
        )

    def load(self):
        """
        Load OCD ballot measure-related models with data scraped from CAL-ACCESS website.
        """
        # Loop over scraped elections
        for scraped_elec in self.get_scraped_elecs():
            # Get or create an OCD election
            ocd_elec, elec_created = self.get_or_create_election(scraped_elec)
            if elec_created and self.verbosity > 2:
                self.log('Created new Election: %s' % ocd_elec.name)

            # Update or create the Election source
            ocd_elec.sources.update_or_create(
                url=scraped_elec.url,
                note='Last scraped on {dt:%Y-%m-%d}'.format(
                    dt=scraped_elec.last_modified,
                )
            )

            # Loop over election's scraped propositions
            for scraped_prop in self.get_scraped_props(scraped_elec):
                try:
                    # Try getting the contest using scraped_id
                    ocd_contest = ocd_elec.ballotmeasurecontests.get(
                        identifiers__scheme='calaccess_measure_id',
                        identifiers__identifier=scraped_prop.scraped_id,
                    )
                except BallotMeasureContest.DoesNotExist:
                    # If not there, create one
                    ocd_contest = self.create_contest(scraped_prop, ocd_elec)
                    # Add the options
                    ocd_contest.options.create(text='yes')
                    ocd_contest.options.create(text='no')
                    # Add the identifiers
                    ocd_contest.identifiers.create(
                        scheme='calaccess_measure_id',
                        identifier=scraped_prop.scraped_id,
                    )
                    if self.verbosity > 2:
                        self.log(
                            'Created new {0}: {1}'.format(
                                ocd_contest._meta.object_name,
                                ocd_contest,
                            )
                        )
                else:
                    # If the contest already exists, make sure the name is up-to-date
                    # because they could change on subsequent scrapes of the SoS website
                    if ocd_contest.name != scraped_prop.name:
                        ocd_contest.name = scraped_prop.name
                        ocd_contest.save()

                # Update or create the Contest source
                ocd_contest.sources.update_or_create(
                    url=scraped_prop.url,
                    note='Last scraped on {dt:%Y-%m-%d}'.format(
                        dt=scraped_prop.last_modified,
                    )
                )
