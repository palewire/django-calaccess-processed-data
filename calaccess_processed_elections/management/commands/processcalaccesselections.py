"""Load OCD elections models with data extracted and scraped from CAL-ACCESS."""
import os

from django.apps import apps
from django.core.management import call_command

from . import LoadOCDElectionsBase


class Command(LoadOCDElectionsBase):
    """
    Load OCD elections models with data extracted and scraped from CAL-ACCESS.
    """

    help = "Load OCD elections models with data extracted and scraped from CAL-ACCESS"

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        # create subdirectory in processed_data_dir, if missing
        filings_data_path = os.path.join(self.processed_data_dir, "relational")
        os.path.isdir(filings_data_path) or os.makedirs(filings_data_path)

        # Start off loading all the data
        self.load()

        # archive
        if self.verbosity > 2:
            self.log(" Archiving OCD processed data files.")
        models_to_archive = apps.get_app_config(
            "calaccess_processed_elections"
        ).get_ocd_models_list()
        for m in models_to_archive:
            call_command("archivecalaccesselectionsfile", m._meta.object_name)

        # Wrap it up
        self.success("Done!")

    def load(self):
        """
        Load all of the processed models.
        """
        # Set options for commands
        options = dict(verbosity=self.verbosity, no_color=self.no_color)

        #
        # Load parties
        #

        call_command("loadocdparties", **options)
        self.duration()

        #
        # Load elections
        #

        call_command("loadocdelections", **options)
        self.duration()

        #
        # Load contests and candidates
        #

        call_command("loadocdcandidatecontests", **options)
        self.duration()

        call_command("loadocdballotmeasurecontests", **options)
        self.duration()

        call_command("loadocdretentioncontests", **options)
        self.duration()

        call_command("loadocdcandidaciesfrom501s", **options)
        self.duration()

        call_command("loadocdincumbentofficeholders", **options)
        self.duration()

        #
        # Merge duplicates
        #

        call_command("mergeocdpersonsbyfilerid", **options)
        self.duration()

        call_command("mergeocdpersonsbycontestandname", **options)
        self.duration()
