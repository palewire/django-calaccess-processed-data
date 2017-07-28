#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for CalAccess base model methods.
"""
from unittest import TestCase
from django.db.models.base import ModelBase
from calaccess_processed.models import Form460Filing


class CalAccessBaseModelTests(TestCase):
    """
    Test for Form460Filing model.
    """
    def test_doc(self):
        """
        Confirm doc method returns a non-empty string.
        """
        doc = Form460Filing().doc()
        self.assertGreater(len(doc), 0)

    def test_field_list(self):
        """
        Confirm field_list method returns a non-empty list.
        """
        fields_list = Form460Filing().get_field_list()
        self.assertGreater(len(fields_list), 0)

    def test_db_table(self):
        """
        Confirm db_table property equals '{app_label}_{model_name}' string.
        """
        db_table_name = '{app_label}_{model_name}'.format(
            **Form460Filing()._meta.__dict__
        )
        self.assertEqual(Form460Filing().db_table, db_table_name)

    def test_klass(self):
        """
        Confirm klass is an instance of ModelBase.
        """
        self.assertIsInstance(Form460Filing().klass, ModelBase)

    def test_klass_name(self):
        """
        Confirm model name equals klass_name string.
        """
        self.assertEqual('Form460Filing', Form460Filing().klass_name)

    def test_klass_group(self):
        """
        Confirm klass_group does not return None.
        """
        self.assertIsNotNone(Form460Filing().klass_name)
