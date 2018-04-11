#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for correcting connection between candidates and parties.
"""
import os
import csv
from django.apps import apps


def candidate_party(candidate_name, year, election_type, office):
    """
    Returns the correct OCD party organization object for a given candidate name, year, election_type and office.

    Returns None if no correction is found.
    """
    from calaccess_processed.models.proxies import OCDPartyProxy

    # Get the path to our corrections file
    app = apps.get_app_config("calaccess_processed")
    module_dir = os.path.abspath(os.path.dirname(app.module.__file__))
    corrections_path = os.path.join(module_dir, 'corrections', "candidate_party.csv")

    # Open up the corrections
    with open(corrections_path, 'r') as f:
        corrections = csv.DictReader(f)
        # Filter down to the ones we've corrected
        corrections = [d for d in corrections if d['party']]

    # Filter down to the ones that match
    matches = [
        d['party'] for d in corrections if (
            d['candidate_name'] == candidate_name and
            str(d['year']) == str(year) and
            d['election_type'] == election_type and
            d['office'] == office
        )
    ]

    # If there's more than one result throw an error
    if len(matches) > 1:
        raise Exception('More than one correction found.')
    # If there's no match return None
    elif len(matches) == 0:
        return None
    # If there's only one match return that
    else:
        return OCDPartyProxy.objects.get_by_name(matches[0])
