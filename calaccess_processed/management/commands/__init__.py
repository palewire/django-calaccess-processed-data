#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base classes for custom management commands.
"""
from __future__ import unicode_literals
import os
import re
import logging
from django.utils import timezone
from django.db.models import Count
from opencivicdata.merge import merge
from django.utils.termcolors import colorize
from django.core.management.base import BaseCommand
from django.core.management import CommandError
from calaccess_raw import get_data_directory
from calaccess_raw.models import RawDataVersion
from calaccess_processed.models import ProcessedDataVersion, OCDDivisionProxy
from opencivicdata.core.management.commands.loaddivisions import load_divisions
logger = logging.getLogger(__name__)


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
            'processed',
        )
        if not os.path.exists(self.processed_data_dir):
            # make the processed data director
            os.makedirs(self.processed_data_dir)
            # set permissions to allow other users to write and execute
            os.chmod(self.processed_data_dir, 0o703)

    def get_or_create_processed_version(self):
        """
        Get or create the current processed version.

        Return a tuple (ProcessedDataVersion object, created), where
        created is a boolean specifying whether a version was created.
        """
        # get the latest raw data version
        try:
            latest_raw_version = RawDataVersion.objects.latest(
                'release_datetime',
            )
        except RawDataVersion.DoesNotExist:
            raise CommandError(
                'No raw CAL-ACCESS data loaded (run `python manage.py '
                'updatecalaccessrawdata`).'
            )

        # check if latest raw version update completed
        if latest_raw_version.update_stalled:
            msg_tmp = 'Update to raw version released at %s did not complete'
            raise CommandError(
                msg_tmp % latest_raw_version.release_datetime.ctime()
            )

        return ProcessedDataVersion.objects.get_or_create(
            raw_version=latest_raw_version,
        )

    def header(self, string):
        """
        Writes out a string to stdout formatted to look like a header.
        """
        logger.debug(string)
        if not getattr(self, 'no_color', None):
            string = colorize(string, fg="cyan", opts=("bold",))
        self.stdout.write(string)

    def log(self, string):
        """
        Writes out a string to stdout formatted to look like a standard line.
        """
        logger.debug(string)
        if not getattr(self, 'no_color', None):
            string = colorize("%s" % string, fg="white")
        self.stdout.write(string)

    def success(self, string):
        """
        Writes out a string to stdout formatted green to communicate success.
        """
        logger.debug(string)
        if not getattr(self, 'no_color', None):
            string = colorize(string, fg="green")
        self.stdout.write(string)

    def warn(self, string):
        """
        Writes string to stdout formatted yellow to communicate a warning.
        """
        logger.warn(string)
        if not getattr(self, 'no_color', None):
            string = colorize(string, fg="yellow")
        self.stdout.write(string)

    def failure(self, string):
        """
        Writes string to stdout formatted red to communicate failure.
        """
        logger.error(string)
        if not getattr(self, 'no_color', None):
            string = colorize(string, fg="red")
        self.stdout.write(string)

    def duration(self):
        """
        Calculates how long command has been running and writes it to stdout.
        """
        duration = timezone.now() - self.start_datetime
        self.stdout.write('Duration: {}'.format(str(duration)))
        logger.debug('Duration: {}'.format(str(duration)))

    def __str__(self):
        return re.sub(r'(.+\.)*', '', self.__class__.__module__)


class LoadOCDModelsCommand(CalAccessCommand):
    """
    Base class for OCD model loading management commands.
    """
    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(LoadOCDModelsCommand, self).handle(*args, **options)
        try:
            self.state_division = OCDDivisionProxy.objects.california()
        except OCDDivisionProxy.DoesNotExist:
            if self.verbosity > 2:
                self.log(' CA state division missing. Loading all U.S. divisions')
            load_divisions('us')

    def merge_persons(self, persons):
        """
        Merge items in persons iterable into one Person object.

        Return the merged Person object.
        """
        # each person will be merged into this one
        keep = persons.pop(0)

        # loop over all the rest
        for i in persons:
            merge(keep, i)
            keep.refresh_from_db()

        # also delete the now duplicated PersonIdentifier objects
        keep_filer_ids = keep.identifiers.filter(scheme='calaccess_filer_id')

        dupe_filer_ids = keep_filer_ids.values("identifier").annotate(
            row_count=Count('id'),
        ).order_by().filter(row_count__gt=1)

        for i in dupe_filer_ids.all():
            # delete all rows with that filer_id
            keep_filer_ids.filter(identifier=i['identifier']).delete()
            # then re-add the one
            keep.identifiers.create(
                scheme='calaccess_filer_id',
                identifier=i['identifier'],
            )

        # and dedupe candidacy records
        # first, make groups by contests with more than one candidacy
        contest_group_q = keep.candidacies.values("contest").annotate(
            row_count=Count('id')
        ).filter(row_count__gt=1)

        # loop over each contest group
        for group in contest_group_q.all():
            cands = keep.candidacies.filter(contest=group['contest'])
            # preference to "qualified" candidacy (from scrape)
            if cands.filter(registration_status='qualified').exists():
                cand_to_keep = cands.filter(registration_status='qualified').all()[0]
            # or the one with the most recent filed_date
            else:
                cand_to_keep = cands.latest('filed_date')

            # loop over all the other candidacies in the group
            for cand_to_discard in cands.exclude(id=cand_to_keep.id).all():
                # assuming the only thing in extras is form501_filing_ids
                if 'form501_filing_ids' in cand_to_discard.extras:
                    for i in cand_to_discard.extras['form501_filing_ids']:
                        self.link_form501_to_candidacy(i, cand_to_keep)
                cand_to_keep.refresh_from_db()

                if 'form501_filing_ids' in cand_to_keep.extras:
                    self.update_candidacy_from_form501s(cand_to_keep)
                cand_to_keep.refresh_from_db()

                # keep the candidate_name, if not already somewhere else
                if (
                    cand_to_discard.candidate_name != cand_to_keep.candidate_name and
                    cand_to_discard.candidate_name != cand_to_keep.person.name and
                    not cand_to_keep.person.other_names.filter(
                        name=cand_to_discard.candidate_name
                    ).exists()
                ):
                    keep.other_names.create(
                        name=cand_to_discard.candidate_name,
                        note='From merge of %s candidacies' % cand_to_keep.contest
                    )
                    cand_to_keep.refresh_from_db()

                # keep the candidacy sources
                if cand_to_discard.sources.exists():
                    for source in cand_to_discard.sources.all():
                        if not cand_to_keep.sources.filter(url=source.url).exists():
                            cand_to_keep.sources.create(
                                url=source.url,
                                note=source.note,
                            )
                        cand_to_keep.refresh_from_db()

                # keep earliest filed_date
                if cand_to_keep.filed_date and cand_to_discard.filed_date:
                    if cand_to_keep.filed_date > cand_to_discard.filed_date:
                        cand_to_keep.filed_date = cand_to_discard.filed_date
                elif cand_to_discard.filed_date:
                    cand_to_keep.filed_date = cand_to_discard.filed_date
                # keep is_incumbent if True
                if not cand_to_keep.is_incumbent and cand_to_discard.is_incumbent:
                    cand_to_keep.is_incumbent = cand_to_discard.is_incumbent
                # assuming not trying to merge candidacies with different parties
                if not cand_to_keep.party and cand_to_discard.party:
                    cand_to_keep.party = cand_to_discard.party

                cand_to_keep.save()
                cand_to_discard.delete()

        keep.refresh_from_db()

        # make sure Person name is same as most recent candidate_name
        latest_candidate_name = keep.candidacies.latest(
            'contest__election__date',
        ).candidate_name
        if keep.name != latest_candidate_name:
            # move current Person.name into other_names
            if not keep.other_names.filter(name=keep.name).exists():
                keep.other_names.create(name=keep.name)
            keep.name = latest_candidate_name
        keep.save()

        return keep
