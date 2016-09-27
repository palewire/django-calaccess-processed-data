import os
import re
import csv
import requests
import urlparse
from time import sleep
from bs4 import BeautifulSoup
from calaccess_raw import get_download_directory
from calaccess_processed.models.campaign import Election, Race, Candidate
from calaccess_processed.management.commands import CalAccessCommand


class ScrapeCommand(CalAccessCommand):
    base_url = 'http://cal-access.ss.ca.gov/'

    def handle(self, *args, **options):
        super(ScrapeCommand, self).handle(*args, **options)
        self.verbosity = int(options['verbosity'])
        results = self.build_results()
        self.process_results(results)

    def build_results(self):
        """
        This method should perform the actual scraping
        and return the structured data.
        """
        raise NotImplementedError

    def process_results(self, results):
        """
        This method receives the structured data returned
        by `build_results` and should process it.
        """
        raise NotImplementedError

    def get(self, url, retries=1):
        """
        Makes a request for a URL and returns the HTML
        as a BeautifulSoup object.
        """
        if self.verbosity > 2:
            self.log(" Retrieving %s" % url)
        tries = 0
        while tries < retries:
            response = requests.get(url)
            if response.status_code == 200:
                return BeautifulSoup(response.text)
            else:
                tries += 1
                sleep(2.0)
        raise HTTPError

    def parse_election_name(self, name):
        """
        Translates a raw election name into
        one of our canonical names.
        """
        name = name.upper()
        if 'PRIMARY' in name:
            return 'PRIMARY'
        elif 'GENERAL' in name:
            return 'GENERAL'
        elif 'SPECIAL RUNOFF' in name:
            return 'SPECIAL_RUNOFF'
        elif 'SPECIAL' in name:
            return 'SPECIAL'
        elif 'RECALL' in name:
            return 'RECALL'
        else:
            return 'OTHER'

    def parse_office_name(self, raw_name):
        """
        Translates a raw office name into one of
        our canonical names and a seat (if available).
        """
        seat = ''
        raw_name = raw_name.upper()
        if 'LIEUTENANT GOVERNOR' in raw_name:
            clean_name = 'LIEUTENANT_GOVERNOR'
        elif 'GOVERNOR' in raw_name:
            clean_name = 'GOVERNOR'
        elif 'SECRETARY OF STATE' in raw_name:
            clean_name = 'SECRETARY_OF_STATE'
        elif 'CONTROLLER' in raw_name:
            clean_name = 'CONTROLLER'
        elif 'TREASURER' in raw_name:
            clean_name = 'TREASURER'
        elif 'ATTORNEY GENERAL' in raw_name:
            clean_name = 'ATTORNEY_GENERAL'
        elif 'SUPERINTENDENT OF PUBLIC INSTRUCTION' in raw_name:
            clean_name = 'SUPERINTENDENT_OF_PUBLIC_INSTRUCTION'
        elif 'INSURANCE COMMISSIONER' in raw_name:
            clean_name = 'INSURANCE_COMMISSIONER'
        elif 'MEMBER BOARD OF EQUALIZATION' in raw_name:
            clean_name = 'BOARD_OF_EQUALIZATION'
            seat = raw_name.split()[-1]
        elif 'SENATE' in raw_name:
            clean_name = 'SENATE'
            seat = raw_name.split()[-1]
        elif 'ASSEMBLY' in raw_name:
            clean_name = 'ASSEMBLY'
            seat = raw_name.split()[-1]
        else:
            clean_name = 'OTHER'
        return {
            'office_name': clean_name,
            'office_seat': seat
        }


class Command(ScrapeCommand):
    """
    Scraper to get the list of candidates per election.
    """
    help = "Scrape links between filers and elections from CAL-ACCESS site"

    def build_results(self):
        self.header("Scraping election candidates")

        url = urlparse.urljoin(
            self.base_url,
            '/Campaign/Candidates/list.aspx?view=certified&electNav=93'
        )
        soup = self.get(url)

        # Get all the links out
        links = soup.findAll('a', href=re.compile(r'^.*&electNav=\d+'))

        # Drop the link that says "prior elections" because it's a duplicate
        links = [
            l for l in links
            if l.find_next_sibling('span').text != 'Prior Elections'
        ]

        # Loop through the links...
        results = []
        for i, link in enumerate(links):
            # .. go and get each page and its data
            url = urlparse.urljoin(self.base_url, link["href"])
            data = self.scrape_page(url)
            # Parse out the name and year
            data['raw_name'] = link.find_next_sibling('span').text.strip()
            data['election_type'] = self.parse_election_name(data['raw_name'])
            data['year'] = int(data['raw_name'][:4])
            # The index value is used to preserve sorting of elections,
            # since multiple elections may occur in a year.
            # BeautifulSoup goes from top to bottom,
            # but the top most election is the most recent so it should
            # have the highest id.
            data['sort_index'] = len(links) - i
            # Add it to the list
            results.append(data)
            # Take a rest
            sleep(0.5)

        # Pass out the data
        return results

    def scrape_page(self, url):
        """
        Pull the elections and candidates from a CAL-ACCESS page.
        """
        # Go and get the page
        soup = self.get(url)

        # Loop through all the election sets on the page
        sections = {}
        for section in soup.findAll('a', {'name': re.compile(r'[a-z]+')}):

            # Check that this data matches the structure we expect.
            section_name_el = section.find('span', {'class': 'hdr14'})

            # If it doesn't just skip this one
            if not section_name_el:
                continue

            # Get the name out of page and key it in the data dictionary
            section_name = section_name_el.text
            sections[section_name] = {}

            # Loop thorugh all the rows in the section table
            for office in section.findAll('td'):

                # Check that this data matches the structure we expect.
                title_el = office.find('span', {'class': 'hdr13'})

                # If it doesn't, just quit
                if not title_el:
                    continue

                # Log what we're up to
                if self.verbosity > 2:
                    self.log('   Scraping office %s' % title_el.text)

                # Pull the candidates out
                people = []
                for p in office.findAll('a', {'class': 'sublink2'}):
                    people.append({
                        'candidate_name': p.text,
                        'candidate_id': re.match(r'.+id=(\d+)', p['href']).group(1)
                    })

                for p in office.findAll('span', {'class': 'txt7'}):
                    people.append({
                        'candidate_name': p.text,
                        'candidate_id':  None
                    })

                # Add it to the data dictionary
                sections[section_name][title_el.text] = people

        return {
            'election_id': int(re.match(r'.+electNav=(\d+)', url).group(1)),
            'data': sections,
        }

    def process_results(self, results):
        """
        Process the scraped data.
        """
        self.log('Processing %s elections.' % len(results))

        # Loop through all the results
        for d in results:

            self.log('  Processing %s' % d['raw_name'])

            election, c = Election.objects.get_or_create(
                election_year=d['year'],
                election_type=d['election_type'],
                election_id=d['election_id'],
                sort_index=d['sort_index'],
            )

            if self.verbosity > 2:
                if c:
                    self.log('  Created %s' % election)

            # Loop through the data list from the scraped page
            for office_dict in d['data'].values():

                # Loop through each of the offices we found there
                for office_name, candidates in office_dict.items():

                    # Create an race object
                    race, c = Race.objects.get_or_create(**self.parse_office_name(office_name))
                    race.election = election
                    race.save()

                    if self.verbosity > 2:
                        if c:
                            self.log('  Created %s' % race)

                    # Loop through each of the candidates
                    for candidate_data in candidates:
                        # See if we have filing information for them
                        candidate = Candidate.objects.filter(
                            filer_id=candidate_data['candidate_id'],
                            office=race.office_name,
                            district=race.office_seat,
                            election_year=election.election_year
                        ).first()

                        # If so, associate them with a race and election object
                        if candidate:
                            candidate.race = race
                            candidate.election = election
                            candidate.save()
