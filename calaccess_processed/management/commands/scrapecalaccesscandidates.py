#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scrape list of certified candidates from the CAL-ACCESS site.
"""
import re
from six.moves.urllib.parse import urljoin
from time import sleep
from calaccess_processed.management.commands import ScrapeCommand
from calaccess_processed.models import (
    ScrapedCandidate,
    CandidateScrapedElection
)


class Command(ScrapeCommand):
    """
    Scrape list of certified candidates for each election on CAL-ACCESS site.
    """
    help = "Scrape certified candidates for each election on the CAL-ACCESS \
    site."

    def flush(self):
        """
        Delete records form related database tables.
        """
        ScrapedCandidate.objects.all().delete()
        CandidateScrapedElection.objects.all().delete()

    def scrape(self):
        """
        Make requests and parse markup into structured data.
        """
        self.header("Scraping election candidates")

        soup = self.get_html(
            '/Campaign/Candidates/list.aspx?view=certified&electNav=93'
        )

        # Get all the links out
        links = soup.findAll('a', href=re.compile(r'^.*&electNav=\d+'))

        # Drop the link that says "prior elections" because it's a duplicate
        links = [
            l for l in links
            if l.find_next_sibling('span').text != 'Prior Elections'
        ]

        # Loop through the links
        results = {}
        for i, link in enumerate(links):
            # Get each page and its data
            url = urljoin(self.base_url, link["href"])
            data = self.scrape_election_page(url)
            # Add the name of the election
            data['name'] = link.find_next_sibling('span').text.strip()
            # The index value is used to preserve sorting of elections,
            # since multiple elections may occur in a year.
            # BeautifulSoup goes from top to bottom,
            # but the top most election is the most recent so it should
            # have the highest id.
            data['sort_index'] = len(links) - i
            # Add it to the list
            results[url] = data
            # Take a rest
            sleep(0.5)

        return results

    def scrape_election_page(self, url):
        """
        Pull the elections and candidates from a CAL-ACCESS page.
        """
        # Go and get the page
        soup = self.get_html(url)

        races = {}
        # Loop through all the election sets on the page
        for section in soup.findAll('a', {'name': re.compile(r'[a-z]+')}):

            # Check that this data matches the structure we expect.
            section_name_el = section.find('span', {'class': 'hdr14'})

            # If it doesn't, skip this one
            if not section_name_el:
                continue

            # Loop through all the rows in the section table
            for office in section.findAll('td'):

                # Check that this data matches the structure we expect.
                title_el = office.find('span', {'class': 'hdr13'})

                # If it doesn't, skip
                if not title_el:
                    continue

                office_name = title_el.text

                # Log what we're up to
                if self.verbosity > 2:
                    self.log('Scraping office %s' % office_name)

                # Pull the candidates out
                candidates = []
                for c in office.findAll('a', {'class': 'sublink2'}):
                    candidates.append({
                        'name': c.text,
                        'scraped_id': re.match(
                            r'.+id=(\d+)',
                            c['href']
                        ).group(1),
                        'url': urljoin(self.base_url, url),
                    })

                for c in office.findAll('span', {'class': 'txt7'}):
                    candidates.append({
                        'name': c.text,
                        'scraped_id': '',
                        'url': urljoin(self.base_url, url),
                    })

                # Add it to the data dictionary
                races[office_name] = candidates

        return {
            'scraped_id': int(re.match(r'.+electNav=(\d+)', url).group(1)),
            'races': races,
            'url': urljoin(self.base_url, url)
        }

    def save(self, results):
        """
        Save results of scrape to related database tables.
        """
        self.log('Processing %s elections.' % len(results))

        # Loop through all the results
        for url, election_data in results.items():

            self.log('Processing %s' % election_data['name'])
            election_obj, c = CandidateScrapedElection.objects.get_or_create(
                name=election_data['name'].strip(),
                scraped_id=election_data['scraped_id'],
                sort_index=election_data['sort_index'],
                url=url,
            )

            if c and self.verbosity > 2:
                self.log('Created %s' % election_obj)

            # Loop through each of the races
            for office_name, candidates in election_data['races'].items():

                # Loop through each of the candidates
                for candidate_data in candidates:

                    # Create the candidate object
                    candidate_obj, c = ScrapedCandidate.objects.get_or_create(
                        name=candidate_data['name'].strip(),
                        scraped_id=candidate_data['scraped_id'],
                        office_name=office_name.strip(),
                        url=candidate_data['url'],
                        election=election_obj,
                    )

                    if c and self.verbosity > 2:
                        self.log('Created %s' % candidate_obj)
