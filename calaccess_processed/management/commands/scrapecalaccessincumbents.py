#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scrape list of incumbent state officials for each election on CAL-ACCESS site.
"""
import re
from six.moves.urllib.parse import urljoin
from datetime import datetime
from time import sleep
from calaccess_processed.management.commands import ScrapeCommand
from calaccess_processed.models import (
    ScrapedIncumbent,
    IncumbentScrapedElection
)


class Command(ScrapeCommand):
    """
    Scrape list of incumbent state officials for each election on CAL-ACCESS site.
    """
    help = "Scrape list of incumbent state officials for each election on CAL-ACCESS site."

    cycle_link_pattern = re.compile(
        r'^/Campaign/Candidates/list\.aspx\?view=incumbent&session=(?P<yr>\d{,4})',
    )

    def flush(self):
        """
        Delete records form related database tables.
        """
        ScrapedIncumbent.objects.all().delete()
        IncumbentScrapedElection.objects.all().delete()

    def scrape(self):
        """
        Make requests and parse markup into structured data.
        """
        self.header("Scraping incumbent state officials")

        soup = self.get_html(
            '/Campaign/Candidates/list.aspx?view=incumbent'
        )

        # build a list of cycle urls
        cycle_links = [
            l['href'] for l in soup.find_all(
                'a',
                href=self.cycle_link_pattern,
            )
        ]

        # Loop through the cycle urls
        results = {}
        for link in cycle_links:
            # Get each page and its data
            url = urljoin(self.base_url, link)
            data = self.scrape_election_page(link)

            # add any new cycle links we found
            for l in data['cycle_links']:
                if l not in cycle_links:
                    cycle_links.append(l)

            # Add the session
            data['session'] = int(
                re.search(self.cycle_link_pattern, link).groupdict()['yr']
            )
            # Add it to the results dict
            results[url] = data
            # Take a rest
            sleep(0.5)

        return results

    def scrape_election_page(self, url):
        """
        Pull the elections and incumbents from a CAL-ACCESS page.
        """
        # Go and get the page
        soup = self.get_html(url)

        data = {
            'cycle_links': [],
            'elections': [],
            'incumbents': [],
        }

        # dedupe the list of cycle links
        for l in soup.find_all('a', href=self.cycle_link_pattern):
            if l['href'] not in data['cycle_links']:
                data['cycle_links'].append(l['href'])

        # get elections
        for span in soup.find_all('span', class_='txt7'):
            match = re.match(
                r'^\d+\. (.+)\s+(?:[A-Z][a-z]+day), (\d{1,2}\/\d{1,2}\/\d{2})$',
                span.text,
            )
            if match:
                data['elections'].append(
                    {
                        'name': match.groups()[0].strip(),
                        'date': datetime.strptime(match.groups()[1], '%m/%d/%y'),
                    }
                )

        # get incumbents
        # Loop through each table of offices
        sections = soup.find_all(
            'table',
            {
                'cellspacing': 0,
                'cellpadding': 4,
                'border': 3,
                'bordercolor': "#3149AA",
                'bgcolor': "#7183C6",
                'width': "100%",
            }
        )
        # Earlier cycle pages don't have incumbents
        if len(sections) > 0:
            for section in sections:
                category = section.find('span', class_='hdr14').text.strip()

                for td in section.find_all('td', width="50%"):
                    office = td.find('span', class_='txt7').text.strip()
                    for a in td.find_all('a', class_='sublink2'):
                        data['incumbents'].append(
                            {
                                'category': category,
                                'office_name': office,
                                'name': a.text.strip(),
                                'url': a['href'],
                                'scraped_id': re.search(
                                    r'&id=(\d+)',
                                    a['href'].strip()
                                ).groups()[0],
                            }
                        )
        return data

    def save(self, results):
        """
        Save results of scrape to related database tables.
        """
        self.log('Processing %s elections.' % len(results))

        # Loop through all the results
        for url, data in results.items():

            self.log('Processing %s session elections' % data['session'])

            # Loop through each election
            for election in data['elections']:
                # Create the election object
                election_obj, created = IncumbentScrapedElection.objects.get_or_create(
                    session=data['session'],
                    url=url,
                    **election
                )
                if created and self.verbosity > 2:
                    self.log('Created %s' % election_obj)

            # Loop through each incumbent
            for incumbent in data['incumbents']:
                # Create the incumbent object
                incumbent_obj, created = ScrapedIncumbent.objects.get_or_create(
                    session=data['session'],
                    **incumbent
                )
                if created and self.verbosity > 2:
                    self.log('Created %s' % incumbent_obj)
