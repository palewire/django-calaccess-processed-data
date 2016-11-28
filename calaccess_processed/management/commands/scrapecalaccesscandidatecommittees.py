/Campaign/Candidates/Detail.aspx?id=1234505

import re
import urlparse
from time import sleep
from calaccess_processed.management.commands import ScrapeCommand
from calaccess_processed.models.scraped import (
    ScrapedCandidate,
    ScrapedCandidateCommittee,
)


class Command(ScrapeCommand):
    """
    
    """
    help = ""

    def flush(self):
        ScrapedCandidateCommittee.objects.all().delete()

    def scrape(self):
        self.header("Scraping election candidates")

        # Set of unique scraped candidate ids
        candidate_ids = set(ScrapedCandidate.objects.values_list(
            'scraped_id', flat=True))

        results = []

        for candidate_id in candidate_ids:
            url = '/Campaign/Candidates/Detail.aspx?id={}'.format(
                candidate_id)
            data = {}
            data['candidate_id'] = candidate_id
            data['commitees'] = self.scrape_candidate_page(url)
            results.append(data)
            sleep(0.5)

        return results

    def scrape_candidate_page(self, url):
        soup = self.get_html(url)

        # Pull the candidate committees
        committees = []

        for table in soup.findAll('table'):
            c = table.find('a', {'class': 'sublink6'})
            if c:
                committees.append({
                    'name': c.text,
                    'scraped_id': re.match(r'.+id=(\d+)', c['href']).group(1)
                })

        return committees

    def save(self, results):
        """
        Add the data to the database.
        """
        self.log('Processing %s committees.' % len(results))

        # Loop through all the results
        for result in results:
            for committee_data in result['committees']:
                committee_data['candidate'] = result['candidate_id']
                committee_obj, c = ScrapedCandidateCommittee.objects.get_or_create(
                    **committee_data
                )
                if c and self.verbosity > 2:
                    self.log('Created %s' % committee_obj)
