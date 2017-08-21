import os
import time
import calculate
from github import Github
from django.apps import apps
from django.conf import settings
from calaccess_processed.management.commands import CalAccessCommand
from django.contrib.humanize.templatetags.humanize import intcomma


class Command(CalAccessCommand):
    help = 'Analyze how many model fields lack documentation'

    def handle(self, *args, **kwargs):
        """
        Make it happen.
        """
        # Loop through all the models and find any fields without docs
        field_count = 0
        missing_list = []
        for m in self.get_model_list():
            field_list = m()._meta.fields
            field_count += len(field_list)
            for f in field_list:
                if not self.has_docs(f):
                    self.log("- [ ] {}".format(f))
                    missing_list.append((m, f))

        # If everything is done, declare victory
        if not missing_list:
            self.success("All %s fields documented!" % field_count)
            return False

        # If not, loop through the missing and create issues
        missing_count = len(missing_list)
        self.failure(
            "%s/%s (%d%%) of fields lack documentation" % (
                intcomma(missing_count),
                intcomma(field_count),
                calculate.percentage(missing_count, field_count)
            )
        )

    def get_model_list(self):
        return apps.get_app_config('elections').models.values() + apps.get_app_config('core').models.values()

    def has_docs(self, field):
        """
        Test if a Django field has some kind of documentation already.

        Returns True or False
        """
        if field.name == 'id':
            return True
        if field.help_text:
            return True
        if field.__dict__['_verbose_name']:
            return True
        return False
