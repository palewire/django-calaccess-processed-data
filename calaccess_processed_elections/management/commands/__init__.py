"""Base classes for custom management commands."""
from django.core.management import call_command

from calaccess_processed_elections.proxies import OCDDivisionProxy
from calaccess_processed.management.commands import CalAccessCommand


class LoadOCDElectionsBase(CalAccessCommand):
    """
    Base class for custom management commands that load the OCD Election model.
    """

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(LoadOCDElectionsBase, self).handle(*args, **options)

        # Verify that OCD divisions have been loaded
        try:
            OCDDivisionProxy.objects.california()
        except OCDDivisionProxy.DoesNotExist:
            if self.verbosity > 2:
                self.log(" CA state division missing. Loading all U.S. divisions")
            call_command("loaddivisions", "us")

    def load_from_proxy(self, proxy):
        """Load OCD Election from scraped proxy model."""
        # Loop through all elections in the proxy
        for scraped_election in proxy.objects.all():

            # Log each one as we go
            if self.verbosity > 1:
                self.log(f"Loading from {scraped_election}")

            # Get or create an election record
            ocd_election, ocd_created = scraped_election.get_or_create_ocd_election()

            # If we made a new one, log it out
            if ocd_created and self.verbosity > 1:
                self.log(f" Created new Election: {ocd_election}")

            # Whether Election is new or not, update EventSource
            ocd_election.sources.update_or_create(
                url=scraped_election.url,
                note="Last scraped on {:%Y-%m-%d}".format(
                    scraped_election.last_modified
                ),
            )
