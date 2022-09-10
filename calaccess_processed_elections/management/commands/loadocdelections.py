"""Load the OCD Election model with data from the scraped CandidateElection model."""
from calaccess_processed_elections.proxies import (
    ScrapedPropositionElectionProxy,
    ScrapedIncumbentElectionProxy,
    ScrapedCandidateElectionProxy,
)
from calaccess_processed_elections.management.commands import LoadOCDElectionsBase


class Command(LoadOCDElectionsBase):
    """Load the OCD Election model with data from the scraped models."""

    help = (
        "Load the OCD Election model with data from the scraped CandidateElection model"
    )

    def handle(self, *args, **options):
        """Make it happen."""
        super(Command, self).handle(*args, **options)

        self.header("Loading Elections from scraped propositions")
        self.load_from_proxy(ScrapedPropositionElectionProxy)

        self.header("Loading Elections from scraped incumbents")
        self.load_from_proxy(ScrapedIncumbentElectionProxy)

        self.header("Loading Elections from scraped candidates")
        self.load_from_proxy(ScrapedCandidateElectionProxy)

        self.success("Done!")
