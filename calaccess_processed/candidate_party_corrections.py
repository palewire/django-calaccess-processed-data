#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Includes correct party affiliation for candidate in specific contests.
"""
corrections = (
    # http://elections.cdn.sos.ca.gov/statewide-elections/2014-primary/updated-contact-info.pdf # noqa
    ('WINSTON, ALMA MARIE', 2014, 'PRIMARY', 'GOVERNOR', 'REPUBLICAN'),
    # http://elections.cdn.sos.ca.gov/statewide-elections/2014-primary/certified-write-in-list.pdf # noqa
    ('WALLS, JIMELLE L.', 2014, 'PRIMARY', 'GOVERNOR', 'NO PARTY PREFERENCE'),
    # http://elections.cdn.sos.ca.gov/statewide-elections/2012-primary/updated-contact-info-cert-list.pdf # noqa
    ('ESPINOSA, GEBY E.', 2014, 'PRIMARY', 'ASSEMBLY 24', 'DEMOCRATIC'),
    # http://elections.cdn.sos.ca.gov/special-elections/2011-sd28/certified-list.pdf
    ('VALENTINE, ROBERT S.', 2011, 'SPECIAL ELECTION', 'STATE SENATE 28', 'REPUBLICAN'),
    # http://cal-access.sos.ca.gov/Campaign/Candidates/Detail.aspx?id=1273672
    ('WALDRON, MARIE', 2018, 'PRIMARY', 'ASSEMBLY 75', 'REPUBLICAN'),
)
