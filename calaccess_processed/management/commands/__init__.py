#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from django.utils.termcolors import colorize
from django.core.management.base import BaseCommand
logger = logging.getLogger(__name__)

class CalAccessCommand(BaseCommand):
    """
    Base management command that provides common functionality for the other commands in this app.
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

    def header(self, string):
        """
        Writes out a string to stdout formatted to look like a header.
        """
        logger.debug(string)
        if not self.no_color:
            string = colorize(string, fg="cyan", opts=("bold",))
        self.stdout.write(string)

    def log(self, string):
        """
        Writes out a string to stdout formatted to look like a standard line.
        """
        logger.debug(string)
        if not self.no_color:
            string = colorize("%s" % string, fg="white")
        self.stdout.write(string)

    def success(self, string):
        """
        Writes out a string to stdout formatted green to communicate success.
        """
        logger.debug(string)
        if not self.no_color:
            string = colorize(string, fg="green")
        self.stdout.write(string)

    def warn(self, string):
        logger.warn(string)
        if not self.no_color:
            string = colorize(string, fg="yellow")
        self.stdout.write(string)

    def failure(self, string):
        """
        Writes out a string to stdout formatted red to communicate failure.
        """
        logger.error(string)
        if not self.no_color:
            string = colorize(string, fg="red")
        self.stdout.write(string)

    def duration(self):
        """
        Calculates how long the command has been running and writes it to stdout.
        """
        duration = datetime.now() - self.start_datetime
        self.stdout.write('Duration: {}'.format(str(duration)))
        logger.debug('Duration: {}'.format(str(duration)))

