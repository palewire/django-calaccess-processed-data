#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Export and archive a .csv file for a given model.
"""
from django.apps import apps
from calaccess_processed.management.commands._archivecalaccessprocessedfile import Command as BaseCommand


class Command(BaseCommand):

    def get_model(self, processed_file):
        model_dict = apps.get_app_config("calaccess_processed_flatfiles").get_flat_proxy_lookup()
        return model_dict[processed_file.file_name]



        # # now do flat files
        # flat_file_list = [
        #     'Candidates', 'BallotMeasures', 'RecallMeasures'
        # ]
        # for f in flat_file_list:
        #     processed_data_file, created = self.processed_version.files.get_or_create(
        #         file_name=f,
        #     )
        #     processed_data_file.process_start_datetime = now()
        #     processed_data_file.save()
        #
        #     call_command('archivecalaccessprocessedfile', f)
        #     processed_data_file.refresh_from_db()
        #     processed_data_file.process_finish_datetime = now()
        #     processed_data_file.save()


    # @property
    # def model(self):
    #     """
    #     Returns the ProcessedDataFile's corresponding database model object.
    #     """
    #     # first, try finding a model with a name that matches the file_name.
    #     try:
    #         model = apps.get_model(
    #             'calaccess_processed',
    #             self.file_name,
    #         )
    #     except LookupError:
    #         # next, try finding a proxy model a name that contains file_name.
    #         try:
    #             model = apps.get_model(
    #                 'calaccess_processed',
    #                 'OCD%sProxy' % self.file_name,
    #             )
    #         except LookupError:
    #             # finally, try finding a model with a plural name
    #             # matches file_name.
    #             # convert file_name from camel case
    #             s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1 \2', self.file_name)
    #             s2 = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', s1).lower()
    #             model_list = [
    #                 m for m in apps.get_models()
    #                 if m._meta.verbose_name_plural == s2
    #             ]
    #             try:
    #                 model = model_list.pop()
    #             except IndexError:
    #                 model = None
    #
    #     return model
