"""Load OCD elections models with data extracted and scraped from CAL-ACCESS."""
import os

from django.apps import apps
from django.core.management import call_command

from calaccess_processed.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Archive flat files of CAL-ACCESS data.
    """

    help = "Archive flat files of CAL-ACCESS data"

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        # then archive
        if self.verbosity > 2:
            self.log(" Archiving OCD processed data files.")

        # create subdirectory in processed_data_dir, if missing
        filings_data_path = os.path.join(self.processed_data_dir, "flat")
        os.path.isdir(filings_data_path) or os.makedirs(filings_data_path)

        # now do flat files
        flat_file_list = apps.get_app_config(
            "calaccess_processed_flatfiles"
        ).get_flat_names_list()
        for f in flat_file_list:
            call_command("archivecalaccessflatfile", f)

        # Wrap it up
        self.success("Done!")
