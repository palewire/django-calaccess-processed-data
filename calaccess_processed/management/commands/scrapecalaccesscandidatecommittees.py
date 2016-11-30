import re
from time import sleep
from calaccess_processed.management.commands import ScrapeCommand
from calaccess_processed.models.scraped import (
    ScrapedCandidate,
    ScrapedCandidateCommittee,
)


class Command(ScrapeCommand):
    """
    Scrape each candidate's committees from the CAL-ACCESS site.
    """
    help = "Scrape each candidate's committees from the CAL-ACCESS site."

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
            data['committees'] = self.scrape_candidate_page(url)
            results.append(data)
            sleep(0.5)

        return results

    def scrape_candidate_page(self, url):
        """
        Pull the committees from a CAL-ACCESS candidate page.
        """
        soup = self.get_html(url)

        committees = []

        for table in soup.findAll('table')[2].findAll('table'):
            # Committees with a link
            c = table.find('a', {'class': 'sublink6'})
            if c:
                committees.append({
                    'name': c.text,
                    'scraped_id': re.match(r'.+id=(\d+)', c['href']).group(1),
                    'status': table.findAll('tr')[1].findAll('td')[1].text
                })
            # Committees with an ID but no link
            else:
                regex = re.compile(r'(.*)\(ID# (\d*)\)')
                c = table.find('span', string=regex)
                if c:
                    matches = re.match(regex, c.text)
                    committees.append({
                        'name': matches.group(1),
                        'scraped_id': matches.group(2),
                        'status': table.findAll('tr')[1].findAll('td')[1].text
                    })

        return committees

    def save(self, results):
        self.log('Processing %s committees.' % len(results))

        for result in results:
            for committee_data in result['committees']:
                # Add the candidate id to the committee data
                committee_data['candidate_id'] = result['candidate_id']
                committee_obj, c = ScrapedCandidateCommittee.objects \
                    .get_or_create(
                        **committee_data
                    )
                if c and self.verbosity > 2:
                    self.log('Created %s' % committee_obj)
