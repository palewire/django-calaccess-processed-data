"""Load data into processed CAL-ACCESS models, archive processed files and ZIP."""
import os

from django.core.management import call_command
from django.core.management.base import CommandError

from calaccess_scraped.models import PropositionElection
from calaccess_processed.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """Load data into processed CAL-ACCESS models, archive processed files and ZIP."""

    help = (
        "Load data into processed CAL-ACCESS models, archive processed files and ZIP."
    )

    def handle(self, *args, **options):
        """Make it happen."""
        # Throw an error if the scraper hasn't been run.
        if not PropositionElection.objects.exists():
            raise CommandError(
                "Sorry. You must first run 'loadcalaccessscrapeddata' from the calaccess_scraped app."
            )

        # Set options
        super(Command, self).handle(*args, **options)

        # Clear it out
        if self.verbosity > 2:
            self.log("Flushing local copies of processed data files.")
        for dirpath, dirnames, filenames in os.walk(self.processed_data_dir):
            file_paths = [os.path.join(dirpath, i) for i in filenames]
            for file_path in file_paths:
                try:
                    os.remove(file_path)
                except OSError:
                    pass

        # then load
        call_command(
            "processcalaccessfilings",
            verbosity=self.verbosity,
            no_color=self.no_color,
        )
        call_command(
            "processcalaccesselections",
            verbosity=self.verbosity,
            no_color=self.no_color,
        )
        call_command(
            "processcalaccessflatfiles",
            verbosity=self.verbosity,
            no_color=self.no_color,
        )

        # then verify
        call_command(
            "verifycalaccessprocesseddata",
            verbosity=self.verbosity,
            no_color=self.no_color,
        )

        self.success("Processing complete")
        self.duration()
