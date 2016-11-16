#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urlparse
from time import sleep
from datetime import datetime
from calaccess_processed.management.commands import ScrapeCommand
from calaccess_processed.models.scraped import (
    PropositionScrapedElection,
    ScrapedProposition,
<<<<<<< HEAD
    ScrapedPropositionCommittee,
=======
    ScrapedCommittee
>>>>>>> 18e88a8780beae17b8a7adb1795e5b9eb2d94c1f
)


class Command(ScrapeCommand):
    """
    Scrape links between filers and propositions from the official CAL-ACCESS site.
    """
    help = "Scrape links between filers and propositions from the official CAL-ACCESS site."

    def flush(self):
<<<<<<< HEAD
        ScrapedPropositionCommittee.objects.all().delete()
=======
        ScrapedCommittee.objects.all().delete()
>>>>>>> 18e88a8780beae17b8a7adb1795e5b9eb2d94c1f
        ScrapedProposition.objects.all().delete()
        PropositionScrapedElection.objects.all().delete()

    def scrape(self):
        self.header("Scraping propositions")

        # Build the link list from the 2013 page because otherwise the
        # other years are hidden under the "Historical" link.
        soup = self.get_html('Campaign/Measures/list.aspx?session=2013')

        # Filter links for uniqueness.
        links = soup.findAll('a', href=re.compile(r'^.*\?session=\d+'))
        links = list(set([link['href'] for link in links]))

        results = []
        for link in links:
            data = self.scrape_year_page(link)
            # Add it to the list
            results.append(data)
            sleep(0.5)

        # Pass it out
        return results

    def scrape_year_page(self, url):
        """
        Scrape data from a CAL-ACCESS page that publishes the list
        of propositions in a particular election year.
        """
        # Get the URL of the year page
        soup = self.get_html(url)

        # Loop through all the tables on the page
        data_dict = {}
        table_list = soup.findAll(
            'table',
            {'id': re.compile(r'ListElections1__[a-z0-9]+')}
        )
        for table in table_list:

            # Pull the title
            election_name = table.select('caption span')[0].text

            # Get a list of the propositions in this table
            prop_links = table.findAll('a')

            # Log what we're up to
            if self.verbosity > 2:
                msg = " Scraped: %s (%s props)"
                msg = msg % (
                    election_name,
                    len(prop_links),
                )
                self.log(msg)

            # Scrape them one by one
            prop_list = [
                self.scrape_prop_page('/Campaign/Measures/%s' % link['href'])
                    for link in prop_links
            ]

            # Add the data to our data dict
            data_dict[election_name] = prop_list

        # Pass the data back out
        return data_dict

    def scrape_prop_page(self, url):
        """
        Scrape data from a proposition detail page
        """
        # Pull the page
        soup = self.get_html(url)

        # Create a data dictionary to put the good stuff in
        data_dict = {}

        # Add the title and id out of the page
        data_dict['name'] = soup.find('span', id='measureName').text

        data_dict['id'] = re.match(r'.+id=(\d+)', url).group(1)

        data_dict['committees'] = []
        # Loop through all the tables on the page
        # which contain the committees on each side of the measure
        for table in soup.findAll('table', cellpadding='4'):

            # Pull the data box
            data = table.findAll('span', {'class': 'txt7'})

            # The URL
            url = table.find('a', {'class': 'sublink2'})

            # The name
            name = url.text

            # ID sometimes refers to xref_filer_id rather than filer_id_raw
            id_ = data[0].text

            # Does the committee support or oppose the measure?
            position = data[1].text.strip()

            # Put together a a data dictionary and add it to the list
            data_dict['committees'].append({
                'name': name,
                'id': id_,
                'position': position
            })

        if self.verbosity > 2:
            msg = " Scraped: %s (%s committees)"
            msg = msg % (
                data_dict['name'],
                len(data_dict['committees'])
            )
            self.log(msg)

        # Pass the data out
        return data_dict

    def save(self, results):
        """
        Add the data to the database.
        """
        # For each year page
        for d in results:

            # For each election on that page
            for election_name, prop_list in d.items():

                # Get or create election object
                election_obj, c = PropositionScrapedElection.objects.get_or_create(
                    name = election_name,
                )

                # Loop through propositions
                for prop_data in prop_list:

                    # Get or create proposition object
                    prop_obj, c = ScrapedProposition.objects.get_or_create(
                        name=prop_data['name'],
                        scraped_id=prop_data['id'],
                        election=election_obj
                    )

                    # Log it
                    if c and self.verbosity > 2:
                        self.log('Created %s' % prop_obj)

                    # Now loop through the committees
                    for committee in prop_data['committees']:

                        # Get or create it
<<<<<<< HEAD
                        committee_obj, c = ScrapedPropositionCommittee.objects.get_or_create(
=======
                        committee_obj, c = ScrapedCommittee.objects.get_or_create(
>>>>>>> 18e88a8780beae17b8a7adb1795e5b9eb2d94c1f
                            name=committee['name'],
                            scraped_id=committee['id'],
                            position=committee['position'],
                            proposition=prop_obj
                        )

                        # Log it
                        if c and self.verbosity > 2:
                            self.log('Created %s' % committee_obj)
