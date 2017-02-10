#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for OpenCivicData base models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_processed import models
from calaccess_raw.admin.base import BaseAdmin


@admin.register(models.Division)
class DivisionAdmin(BaseAdmin):
    """
    Custom admin for the Division model.
    """
    list_display = (
        'name',
        'subtype1',
        'subtype2',
    )
    list_filter = (
        'subtype1',
        'subtype2',
    )


@admin.register(models.Jurisdiction)
class JurisdictionAdmin(BaseAdmin):
    """
    Custom admin for Jurisdiction model.
    """
    pass



@admin.register(models.LegislativeSession)
class LegislativeSessionAdmin(BaseAdmin):
    """
    Custom admin for LegislativeSession model.
    """
    pass


@admin.register(models.Membership)
class MembershipAdmin(BaseAdmin):
    """
    Custom admin for the Membership model.
    """
    pass


@admin.register(models.Organization)
class OrganizationAdmin(BaseAdmin):
    """
    Custom admin for the Organization model.
    """
    list_display = (
        'name',
        'parent',
        'jurisdiction',
        'classification'
    )
    list_filter = (
        'classification',
    )


@admin.register(models.Person)
class PersonAdmin(BaseAdmin):
    """
    Custom admin for the Person model.
    """
    pass


@admin.register(models.Post)
class PostAdmin(BaseAdmin):
    """
    Custom admin for the Post model.
    """
    list_display = (
        "label",
        "organization",
        "role",
    )
    list_filter = (
        "role",
        "organization"
    )
