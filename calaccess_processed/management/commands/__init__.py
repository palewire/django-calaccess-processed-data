"""Base classes for custom management commands."""
import os
import re

from django.utils import timezone
from django.utils.termcolors import colorize
from django.core.management.base import BaseCommand
from calaccess_raw import get_data_directory


class CalAccessCommand(BaseCommand):
    """
    Base class for all custom CalAccess-related management commands.
    """

    def handle(self, *args, **options):
        """
        Sets options common to all commands.

        Any command subclassing this object should implement its own
        handle method, as is standard in Django, and run this method
        via a super call to inherit its functionality.
        """
        # Set global options
        self.verbosity = options.get("verbosity")
        self.no_color = options.get("no_color")

        # Start the clock
        self.start_datetime = timezone.now()

        # set up processed data directory
        self.data_dir = get_data_directory()
        self.processed_data_dir = os.path.join(
            self.data_dir,
            "processed",
        )
        if not os.path.exists(self.processed_data_dir):
            # make the processed data director
            os.makedirs(self.processed_data_dir)

    def header(self, string):
        """
        Writes out a string to stdout formatted to look like a header.
        """
        if not getattr(self, "no_color", None):
            string = colorize(string, fg="cyan", opts=("bold",))
        self.stdout.write(string)

    def log(self, string):
        """
        Writes out a string to stdout formatted to look like a standard line.
        """
        if not getattr(self, "no_color", None):
            string = colorize("%s" % string, fg="white")
        self.stdout.write(string)

    def success(self, string):
        """
        Writes out a string to stdout formatted green to communicate success.
        """
        if not getattr(self, "no_color", None):
            string = colorize(string, fg="green")
        self.stdout.write(string)

    def warn(self, string):
        """
        Writes string to stdout formatted yellow to communicate a warning.
        """
        if not getattr(self, "no_color", None):
            string = colorize(string, fg="yellow")
        self.stdout.write(string)

    def failure(self, string):
        """
        Writes string to stdout formatted red to communicate failure.
        """
        if not getattr(self, "no_color", None):
            string = colorize(string, fg="red")
        self.stdout.write(string)

    def duration(self):
        """
        Calculates how long command has been running and writes it to stdout.
        """
        duration = timezone.now() - self.start_datetime
        self.stdout.write("Duration: {}".format(str(duration)))

    def __str__(self):
        return re.sub(r"(.+\.)*", "", self.__class__.__module__)
