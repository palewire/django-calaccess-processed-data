#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import logging
import requests
from time import sleep
from bs4 import BeautifulSoup
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


class ScrapeCommand(CalAccessCommand):
    """
    Base management command for scraping the CAL-ACCESS website.
    """
    base_url = 'http://cal-access.ss.ca.gov/'

    def handle(self, *args, **options):
        super(ScrapeCommand, self).handle(*args, **options)
        self.verbosity = int(options['verbosity'])
        results = self.build_results()
        self.process_results(results)

    def build_results(self):
        """
        This method should perform the actual scraping
        and return the structured data.
        """
        raise NotImplementedError

    def process_results(self, results):
        """
        This method receives the structured data returned
        by `build_results` and should process it.
        """
        raise NotImplementedError

    def get(self, url, retries=1):
        """
        Makes a request for a URL and returns the HTML
        as a BeautifulSoup object.
        """
        if self.verbosity > 2:
            self.log(" Retrieving %s" % url)
        tries = 0
        while tries < retries:
            response = requests.get(url)
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
            else:
                tries += 1
                sleep(2.0)
        raise urllib2.HTTPError

    def parse_election_name(self, name):
        """
        Translates a raw election name into
        one of our canonical names.
        """
        name = name.upper()
        if 'PRIMARY' in name:
            return 'PRIMARY'
        elif 'GENERAL' in name:
            return 'GENERAL'
        elif 'SPECIAL RUNOFF' in name:
            return 'SPECIAL_RUNOFF'
        elif 'SPECIAL' in name:
            return 'SPECIAL'
        elif 'RECALL' in name:
            return 'RECALL'
        else:
            return 'OTHER'

    def parse_office_name(self, raw_name):
        """
        Translates a raw office name into one of
        our canonical names and a seat (if available).
        """
        seat = ''
        raw_name = raw_name.upper()
        if 'LIEUTENANT GOVERNOR' in raw_name:
            clean_name = 'LIEUTENANT_GOVERNOR'
        elif 'GOVERNOR' in raw_name:
            clean_name = 'GOVERNOR'
        elif 'SECRETARY OF STATE' in raw_name:
            clean_name = 'SECRETARY_OF_STATE'
        elif 'CONTROLLER' in raw_name:
            clean_name = 'CONTROLLER'
        elif 'TREASURER' in raw_name:
            clean_name = 'TREASURER'
        elif 'ATTORNEY GENERAL' in raw_name:
            clean_name = 'ATTORNEY_GENERAL'
        elif 'SUPERINTENDENT OF PUBLIC INSTRUCTION' in raw_name:
            clean_name = 'SUPERINTENDENT_OF_PUBLIC_INSTRUCTION'
        elif 'INSURANCE COMMISSIONER' in raw_name:
            clean_name = 'INSURANCE_COMMISSIONER'
        elif 'MEMBER BOARD OF EQUALIZATION' in raw_name:
            clean_name = 'BOARD_OF_EQUALIZATION'
            seat = raw_name.split()[-1]
        elif 'SENATE' in raw_name:
            clean_name = 'SENATE'
            seat = raw_name.split()[-1]
        elif 'ASSEMBLY' in raw_name:
            clean_name = 'ASSEMBLY'
            seat = raw_name.split()[-1]
        else:
            clean_name = 'OTHER'
        return {
            'office_name': clean_name,
            'office_seat': seat
        }
