#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import urllib
import urllib2
import logging
import urlparse
import requests
from time import sleep
from bs4 import BeautifulSoup
from django.conf import settings
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
    cache_dir = os.path.join(
        settings.BASE_DIR,
        ".scraper_cache"
    )

    def handle(self, *args, **options):
        super(ScrapeCommand, self).handle(*args, **options)
        os.path.exists(self.cache_dir) or os.mkdir(self.cache_dir)
        results = self.build_results()
        #self.process_results(results)

    def get(self, url, retries=1, base_url=None):
        """
        Makes a request for a URL and returns the HTML as a BeautifulSoup object.
        """
        cache_path = os.path.join(self.cache_dir, urllib.url2pathname(url.strip("/")))
        if os.path.exists(cache_path):
            if self.verbosity > 2:
                self.log(" Returning cached {}".format(cache_path))
            html = open(cache_path, 'r').read()
            return BeautifulSoup(html, "html.parser")
        tries = 0
        while tries < retries:
            if self.verbosity > 2:
                self.log(" Retrieving {}".format(url))
            full_url = urlparse.urljoin(
                base_url or self.base_url,
                url,
            )
            response = requests.get(full_url)
            if response.status_code == 200:
                html = response.text
                if self.verbosity > 2:
                    self.log(" Writing to cache {}".format(cache_path))
                cache_subdir = os.path.dirname(cache_path)
                os.path.exists(cache_subdir) or os.makedirs(cache_subdir)
                with open(cache_path, 'w') as f:
                    f.write(html)
                return BeautifulSoup(html, "html.parser")
            else:
                if self.verbosity > 2:
                    self.log("Request failed. Retrying.")
                tries += 1
                sleep(2.0)
        raise urllib2.HTTPError

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
