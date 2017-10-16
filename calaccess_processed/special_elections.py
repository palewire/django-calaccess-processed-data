#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Includes a mapping of special election names to dates.
"""
# This list was compiled from CAL-ACCESS:
# http://cal-access.sos.ca.gov/Campaign/Candidates/

# And also the documents available from the Secretary of State site:
# * http://www.sos.ca.gov/elections/prior-elections/special-elections/
# * http://elections.cdn.sos.ca.gov/special-elections/pdf/special-elections-history.pdf

names_to_dates = (
    ('2017 SPECIAL RUNOFF (ASSEMBLY 51)', '2017-12-5'),
    ('2017 SPECIAL ELECTION (ASSEMBLY 51)', '2017-10-3'),
    ('2016 SPECIAL ELECTION (ASSEMBLY 31)', '2016-4-5'),
    ('2015 SPECIAL RUNOFF (STATE SENATE 07)', '2015-5-19'),
    ('2015 SPECIAL ELECTION (STATE SENATE 07)', '2015-3-17'),
    ('2015 SPECIAL ELECTION (STATE SENATE 21)', '2015-3-17'),
    ('2015 SPECIAL ELECTION (STATE SENATE 37)', '2015-3-17'),
    ('2014 SPECIAL ELECTION (STATE SENATE 35)', '2014-12-9'),
    ('2014 SPECIAL ELECTION (STATE SENATE 23)', '2014-3-25'),
    ('2013 SPECIAL ELECTION (ASSEMBLY 54)', '2013-12-3'),
    ('2013 SPECIAL RUNOFF (ASSEMBLY 45)', '2013-11-19'),
    ('2013 SPECIAL ELECTION (ASSEMBLY 45)', '2013-9-17'),
    ('2013 SPECIAL RUNOFF (ASSEMBLY 52)', '2013-9-24'),
    ('2013 SPECIAL ELECTION (ASSEMBLY 52)', '2013-7-23'),
    ('2013 SPECIAL ELECTION (STATE SENATE 26)', '2013-9-17'),
    ('2013 SPECIAL RUNOFF (STATE SENATE 16)', '2013-7-23'),
    ('2013 SPECIAL ELECTION (STATE SENATE 16)', '2013-5-21'),
    ('2013 SPECIAL ELECTION (ASSEMBLY 80)', '2013-5-21'),
    ('2013 SPECIAL RUNOFF (STATE SENATE 32)', '2013-5-14'),
    ('2013 SPECIAL ELECTION (STATE SENATE 32)', '2013-3-12'),
    ('2013 SPECIAL ELECTION (STATE SENATE 40)', '2013-3-12'),
    ('2013 SPECIAL ELECTION (STATE SENATE 04)', '2013-1-8'),
    ('2012 SPECIAL ELECTION (STATE SENATE 04)', '2012-11-6'),
    ('2011 SPECIAL RUNOFF (ASSEMBLY 04)', '2011-5-3'),
    ('2011 SPECIAL ELECTION (ASSEMBLY 04)', '2011-3-8'),
    ('2011 SPECIAL ELECTION (STATE SENATE 28)', '2011-2-15'),
    ('2011 SPECIAL ELECTION (STATE SENATE 17)', '2011-2-15'),
    ('2011 SPECIAL RUNOFF (STATE SENATE 01)', '2011-1-4'),
    ('2010 SPECIAL ELECTION (STATE SENATE 01)', '2010-11-2'),
    ('2010 SPECIAL RUNOFF (STATE SENATE 15)', '2010-8-17'),
    ('2010 SPECIAL ELECTION (STATE SENATE 15)', '2010-6-22'),
    ('2010 SPECIAL RUNOFF (STATE SENATE 37)', '2010-6-8'),
    ('2010 SPECIAL ELECTION (STATE SENATE 37)', '2010-4-13'),
    ('2010 SPECIAL RUNOFF (ASSEMBLY 43)', '2010-6-8'),
    ('2010 SPECIAL ELECTION (ASSEMBLY 43)', '2010-4-13'),
    ('2010 SPECIAL RUNOFF (ASSEMBLY 72)', '2010-1-12'),
    ('2009 SPECIAL ELECTION (ASSEMBLY 72)', '2009-11-17'),
    ('2009 SPECIAL ELECTION (ASSEMBLY 51)', '2009-9-1'),
    ('2009 SPECIAL RUNOFF (STATE SENATE 26)', '2009-5-19'),
    ('2009 SPECIAL ELECTION (STATE SENATE 26)', '2009-3-24'),
    ('2008 SPECIAL RUNOFF (ASSEMBLY 55)', '2008-2-5'),
    ('2007 SPECIAL ELECTION (ASSEMBLY 55)', '2007-12-11'),
    ('2007 SPECIAL ELECTION (ASSEMBLY 39)', '2007-5-15'),
    ('2006 SPECIAL RUNOFF (STATE SENATE 35)', '2006-6-6'),
    ('2006 SPECIAL ELECTION (STATE SENATE 35)', '2006-4-11'),
    ('2005 SPECIAL ELECTION (ASSEMBLY 53)', '2005-9-13'),
    ('2003 SPECIAL ELECTION (GOVERNOR)', '2003-10-7'),
    ('2001 SPECIAL ELECTION (ASSEMBLY 49)', '2001-5-15'),
    ('2001 SPECIAL RUNOFF (ASSEMBLY 65)', '2001-4-3'),
    ('2001 SPECIAL ELECTION (ASSEMBLY 65)', '2001-2-6'),
    ('2001 SPECIAL ELECTION (STATE SENATE 24)', '2001-3-6'),
)

names_to_dates_dict = dict(t for t in names_to_dates)
