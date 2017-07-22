#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from django.db import models
from opencivicdata.core.models import Person


class OCDPersonProxy(Person):
    """
    A proxy on the OCD Person model with helper methods.
    """
    class Meta:
        """
        Make this a proxy model.
        """
        proxy = True

    def update_name(self):
        """
        Update name field to the latest candidate record.
        """
        # Get the latest candidate name
        latest_candidate_name = self.candidacies.latest('contest__election__date').candidate_name
        # If the latest candidate name doesn't match the current name
        if self.name != latest_candidate_name:
            # Move the current name into other_names
            if not self.other_names.filter(name=person.name).exists():
                self.other_names.create(name=self.name)
            # Reset the main one
            self.name = latest_candidate_name
            # Save out.
            self.save()
