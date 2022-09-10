"""Export and archive a .csv file for a given model."""
import os

from django.apps import apps
from calaccess_raw import get_data_directory

from calaccess_processed.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Export and archive a .csv file for a given model.
    """

    help = "Export and archive a .csv file for a given model."

    def add_arguments(self, parser):
        """
        Adds custom arguments specific to this command.
        """
        super(Command, self).add_arguments(parser)
        parser.add_argument("model_name", help="Name of the model to archive")

    def get_model(self, processed_file):
        """
        Get the model linked to this processed file record.
        """
        raise NotImplementedError

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        # Parse model name
        self.model_name = options["model_name"]

        # Log out what we're doing ...
        self.log(" Archiving %s.csv" % self.model_name)

        # Get the data obj that is paired with the processed_file obj
        lookup = apps.get_app_config("calaccess_processed").get_processed_file_lookup()
        data_model = lookup[self.model_name]

        # Figure out the path where we will save the file
        csv_dir = os.path.join(
            get_data_directory(), "processed", data_model().klass_group.lower()
        )
        os.path.exists(csv_dir) or os.mkdir(csv_dir)
        csv_name = f"{self.model_name}.csv"
        csv_path = os.path.join(csv_dir, csv_name)

        # Export a new one
        try:
            copy_to_fields = tuple(i[0] for i in data_model.copy_to_fields)
        except AttributeError:
            copy_to_fields = tuple()
        data_model.objects.to_csv(csv_path, *copy_to_fields)
