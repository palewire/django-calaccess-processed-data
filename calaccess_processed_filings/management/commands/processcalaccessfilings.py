"""Load and archive the CAL-ACCESS Filing and FilingVersion models."""
import os

from django.apps import apps
from django.db import connection
from django.core.management import call_command

from calaccess_processed.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Load and archive the CAL-ACCESS Filing and FilingVersion models.
    """

    help = "Load and archive the CAL-ACCESS Filing and FilingVersion models."

    def handle(self, *args, **options):
        """Make it happen."""
        super(Command, self).handle(*args, **options)

        # create subdirectory in processed_data_dir, if missing
        filings_data_path = os.path.join(self.processed_data_dir, "filings")
        os.path.isdir(filings_data_path) or os.makedirs(filings_data_path)

        self.handle_models("version")
        self.handle_models("filing")

    def handle_models(self, model_type):
        """Handle logic for loading models of model_type."""
        model_list = self.get_model_list(model_type)
        if len(model_list) > 0:
            if self.verbosity >= 2:
                self.log(f" Loading {len(model_list)} {model_type} models.")
            self.load_model_list(model_list)

            # archive
            for m in model_list:
                call_command("archivecalaccessfilingsfile", m._meta.object_name)

    def get_model_list(self, model_type):
        """Return a list of models of the specified type to be loaded.

        model_type must be "version" of "filing".
        """
        model_list = apps.get_app_config(
            "calaccess_processed_filings"
        ).get_filing_models()

        if model_type == "version":
            models_to_load = [m for m in model_list if "Version" in str(m)]
        elif model_type == "filing":
            models_to_load = [m for m in model_list if "Version" not in str(m)]
        else:
            raise ValueError('model_type must be "version" or "filing".')
        return models_to_load

    def load_model_list(self, model_list):
        """Iterate over the given list of models, loading each one."""
        # iterate over all of filing models
        for m in model_list:

            # flush the processed model
            if self.verbosity > 2:
                self.log(f" Truncating {m._meta.db_table}")
            with connection.cursor() as c:
                c.execute(
                    f'TRUNCATE TABLE "{m._meta.db_table}" RESTART IDENTITY CASCADE'
                )

            # load the processed model
            if self.verbosity > 2:
                self.log(f" Loading {m._meta.db_table}")
            m.objects.load()
