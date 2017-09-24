#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from django.contrib.postgres.fields import JSONField
from django.db.models import Func, IntegerField


class JSONArrayLength(Func):
    """
    Returns the length of a JSON array.
    """
    function = 'JSONB_ARRAY_LENGTH'
    output_field = IntegerField()


class JSONExtractPath(Func):
    """
    Returns JSON value pointed to by key.
    """
    template = "JSONB_EXTRACT_PATH(%(expressions)s, '%(key)s')"
    output_field = JSONField()

    def __init__(self, expression, key):
        """
        Create an instance.
        """
        super(JSONExtractPath, self).__init__(expression, key=key)


class MaxFromJSONIntegerArray(Func):
    """
    Return the maximum value of an array of integers in key.
    """
    template = "(SORT_DESC(ARRAY(SELECT JSONB_ARRAY_ELEMENTS_TEXT(%(expressions)s->'%(key)s')::int)::int[]))[1]"
    output_field = IntegerField()

    def __init__(self, expression, key):
        """
        Create an instance.
        """
        super(MaxFromJSONIntegerArray, self).__init__(expression, key=key)
