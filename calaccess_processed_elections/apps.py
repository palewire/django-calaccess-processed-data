#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic configuration for the application.
"""
from __future__ import unicode_literals, absolute_import
import os
import collections
from django.apps import apps
from django.apps import AppConfig


class CalAccessProcessedElectionsConfig(AppConfig):
    """
    Application configuration.
    """
    name = 'calaccess_processed_elections'
    verbose_name = "CAL-ACCESS processed data: Elections"
    # Where SQL files are stored in this application
    sql_directory_path = os.path.join(os.path.dirname(__file__), 'sql')

    def get_ocd_models_list(self):
        return list(self.get_ocd_models_dict().keys())

    def get_ocd_models_dict(self):
        """
        Returns a list of the models that should be saved in our archive.
        """
        from . import proxies
        ocd_core = apps.get_app_config('core')
        ocd_elections = apps.get_app_config('elections')
        return collections.OrderedDict({
            ocd_core.get_model('Division'): proxies.OCDDivisionProxy,
            ocd_core.get_model('Organization'): proxies.OCDOrganizationProxy,
            ocd_core.get_model('OrganizationIdentifier'): proxies.OCDOrganizationIdentifierProxy,
            ocd_core.get_model('OrganizationName'): proxies.OCDOrganizationNameProxy,
            ocd_core.get_model('Jurisdiction'): proxiesOCDJurisdictionProxy,
            ocd_core.get_model('Post'): proxies.OCDPostProxy,
            ocd_core.get_model('Person'): proxies.OCDPersonProxy,
            ocd_core.get_model('PersonIdentifier'): proxies.OCDPersonIdentifierProxy,
            ocd_core.get_model('PersonName'): proxies.OCDPersonNameProxy,
            ocd_core.get_model('Membership'): proxies.OCDMembershipProxy,
            ocd_elections.get_model('Election'): proxies.OCDElectionProxy,
            ocd_elections.get_model('ElectionIdentifier'): proxies.OCDElectionIdentifierProxy,
            ocd_elections.get_model('ElectionSource'): proxies.OCDElectionSourceProxy,
            ocd_elections.get_model('Candidacy'): proxies.OCDCandidacyProxy,
            ocd_elections.get_model('CandidacySource'): proxies.OCDCandidacySourceProxy,
            ocd_elections.get_model('BallotMeasureContest'): proxies.OCDBallotMeasureContestProxy,
            ocd_elections.get_model('BallotMeasureContestOption'): proxies.OCDBallotMeasureContestOptionProxy,
            ocd_elections.get_model('BallotMeasureContestIdentifier'): proxies.OCDBallotMeasureContestIdentifierProxy,
            ocd_elections.get_model('BallotMeasureContestSource'): proxies.OCDBallotMeasureContestSourceProxy,
            ocd_elections.get_model('RetentionContest'): proxies.OCDRetentionContestProxy,
            ocd_elections.get_model('RetentionContestOption'): proxies.OCDRetentionContestOptionProxy,
            ocd_elections.get_model('RetentionContestIdentifier'): proxies.OCDRetentionContestIdentifierProxy,
            ocd_elections.get_model('RetentionContestSource'): proxies.OCDRetentionContestSourceProxy,
            ocd_elections.get_model('CandidateContest'): proxies.OCDCandidateContestProxy,
            ocd_elections.get_model('CandidateContestPost'): proxies.OCDCandidateContestPostProxy,
            ocd_elections.get_model('CandidateContestSource'): proxies.OCDCandidateContestSourceProxy
        })
