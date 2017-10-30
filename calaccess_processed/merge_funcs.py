#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Proxy models for augmenting our source data tables with methods useful for processing.
"""
from __future__ import unicode_literals
from calaccess_processed.models import OCDCandidacyProxy, OCDPersonProxy
from django.db.models import Count
from opencivicdata.merge import merge


def merge_persons(persons):
    """
    Merge items in persons iterable into one Person object, which is returned.
    """
    # each person will be merged into this one
    keep = persons.pop(0)
    if keep.__class__ != OCDPersonProxy:
        keep.__class__ = OCDPersonProxy

    # loop over all the rest
    for i in persons:
        if i.__class__ != OCDPersonProxy:
            i.__class__ = OCDPersonProxy
        merge(keep, i)
        keep.refresh_from_db()

    dedupe_person_ids(keep)
    dedupe_person_candidacies(keep)
    keep.refresh_from_db()

    # make sure Person name is same as most recent candidate_name
    latest_candidate_name = keep.candidacies.latest(
        'contest__election__date',
    ).candidate_name
    if keep.name != latest_candidate_name:
        # move current Person.name into other_names
        keep.add_other_name(keep.name, 'Updated current name in merge')
        keep.name = latest_candidate_name
    keep.save()

    return keep


def dedupe_person_ids(person):
    """
    Remove duplicate PersonIdentifier objects linked to person.
    """
    filer_ids = person.identifiers.filter(scheme='calaccess_filer_id')

    dupe_filer_ids = filer_ids.values("identifier").annotate(
        row_count=Count('id'),
    ).order_by().filter(row_count__gt=1)

    for i in dupe_filer_ids.all():
        # delete all rows with that filer_id
        person.identifiers.filter(identifier=i['identifier']).delete()
        # then re-add the one
        person.identifiers.create(
            scheme='calaccess_filer_id',
            identifier=i['identifier'],
        )

    return person


def dedupe_person_candidacies(person):
    """
    Remove duplicate Candidacy objects linked to person.
    """
    # first, make groups by contests with more than one candidacy
    contest_group_q = person.candidacies.values("contest").annotate(
        row_count=Count('id')
    ).filter(row_count__gt=1)

    # loop over each contest group
    for group in contest_group_q.all():
        cands = person.candidacies.filter(contest=group['contest'])
        # preference to "qualified" candidacy (from scrape)
        if cands.filter(registration_status='qualified').exists():
            cand_to_keep = cands.filter(registration_status='qualified').all()[0]
        # or the one with the most recent filed_date
        else:
            cand_to_keep = cands.latest('filed_date')

        cand_to_keep.__class__ = OCDCandidacyProxy

        # loop over all the other candidacies in the group
        for cand_to_discard in cands.exclude(id=cand_to_keep.id).all():
            # assuming there's nothing else to preserve in extras
            # besides form501_filing_ids
            if 'form501_filing_ids' in cand_to_discard.extras:
                for i in cand_to_discard.extras['form501_filing_ids']:
                    cand_to_keep.link_form501(i)
            cand_to_keep.refresh_from_db()

            if 'form501_filing_ids' in cand_to_keep.extras:
                cand_to_keep.update_from_form501()
            cand_to_keep.refresh_from_db()

            # keep the candidate_name, if not already somewhere else
            if (
                cand_to_discard.candidate_name != cand_to_keep.candidate_name and
                cand_to_discard.candidate_name != cand_to_keep.person.name and
                not cand_to_keep.person.other_names.filter(
                    name=cand_to_discard.candidate_name
                ).exists()
            ):
                person.other_names.create(
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

    return person
