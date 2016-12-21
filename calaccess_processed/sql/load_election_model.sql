-- first, insert primary and general elections 
-- by joining candidate elections to ballot proposition elections
INSERT INTO calaccess_processed_election (
    election_type,
    office,
    district,
    election_date
)
SELECT 
    cand.election_type,
    cand.office,
    cand.district,
    prop.election_date
FROM (
    SELECT 
        -- extract the four-digit year, cast as an int
        substring(name from '\d{4}')::INT AS year,
        CASE 
            WHEN name LIKE '%PRIMARY%' THEN 'P'
            WHEN name LIKE '%GENERAL%' THEN 'G'
            WHEN name LIKE '%RECALL%' THEN 'R'
            ELSE NULL
        END AS election_type,
        CASE
            WHEN name LIKE '%ASSEMBLY%' THEN 'ASM'
            WHEN name LIKE '%STATE SENATE%' THEN 'SEN'
            WHEN name LIKE '%GOVERNOR%' THEN 'GOV'
            ELSE NULL
        END AS office,
        -- extract the two digit chars found in the parenthesis, if any
        substring(name from '^\d{4}\s.+\(.+(\d{2})\)$')::INT AS district
    FROM calaccess_processed_candidatescrapedelection
    WHERE name NOT LIKE '%SPECIAL%'
) AS cand
JOIN (
    SELECT 
        substring(name from '\d{4}')::INT AS year,
        substring(name from '\d{4}\s([A-Z])') AS election_type,
        (regexp_matches(name, '^([A-Z]+\s\d{1,2},\s\d{4})\s.+$'))[1]::DATE AS election_date
    FROM calaccess_processed_propositionscrapedelection
    WHERE name NOT LIKE '%SPECIAL%'
    -- for some reason the CAL-ACCESS ballot props page has two "primary"
    -- elections for 2008, so exclude this one
    AND name <> 'JUNE 3, 2008 PRIMARY'
) AS prop
ON cand.year = prop.year
AND cand.election_type = prop.election_type;

-- then insert all the special elections
-- this list is compiled from the candidate elections scraped from CAL-ACCESS: http://cal-access.ss.ca.gov/Campaign/Candidates/
-- and also here: http://www.sos.ca.gov/elections/prior-elections/special-elections/
-- and here: http://elections.cdn.sos.ca.gov/special-elections/pdf/special-elections-history.pdf
INSERT INTO calaccess_processed_election (
    election_type,
    office,
    district,
    election_date
) VALUES 
    ('SE', 'ASM', 31, '2016-4-5'),
    ('SR', 'SEN', 7,  '2015-5-19'),
    ('SE', 'SEN', 7,  '2015-3-17'),
    ('SE', 'SEN', 21, '2015-3-17'),
    ('SE', 'SEN', 37, '2015-3-17'),
    ('SE', 'SEN', 35, '2014-12-9'),
    ('SE', 'SEN', 23, '2014-3-25'),
    ('SE', 'ASM', 54, '2013-12-3'),
    ('SR', 'ASM', 45, '2013-11-19'),
    ('SE', 'ASM', 45, '2013-9-17'),
    ('SE', 'SEN', 26, '2013-9-17'),
    ('SR', 'ASM', 52, '2013-9-24'),
    ('SE', 'ASM', 52, '2013-7-23'),
    ('SE', 'ASM', 80, '2013-5-21'),
    ('SR', 'SEN', 16, '2013-7-23'),
    ('SE', 'SEN', 16, '2013-5-21'),
    ('SR', 'SEN', 32, '2013-5-14'),
    ('SE', 'SEN', 32, '2013-3-12'),
    ('SE', 'SEN', 40, '2013-3-12'),
    ('SE', 'SEN', 4,  '2013-1-8'),
    ('SE', 'SEN', 4,  '2012-11-6'),
    ('SR', 'ASM', 4,  '2011-5-3'),
    ('SE', 'ASM', 4,  '2011-3-8'),
    ('SE', 'SEN', 17, '2011-2-15'),
    ('SE', 'SEN', 28, '2011-2-15'),
    ('SR', 'SEN', 1,  '2011-1-4'),
    ('SE', 'SEN', 1,  '2010-11-2'),
    ('SR', 'SEN', 15, '2010-8-17'),
    ('SE', 'SEN', 15, '2010-6-22'),
    ('SR', 'ASM', 43, '2010-6-8'),
    ('SE', 'ASM', 43, '2010-4-13'),
    ('SR', 'SEN', 37, '2010-6-8'),
    ('SE', 'SEN', 37, '2010-4-13'),
    ('SR', 'ASM', 72, '2010-1-12'),
    ('SE', 'ASM', 72, '2009-11-17'),
    ('SE', 'ASM', 51, '2009-9-1'),
    ('SR', 'SEN', 26, '2009-5-19'),
    ('SE', 'SEN', 26, '2009-3-24'),
    ('SR', 'ASM', 55, '2008-2-5'),
    ('SE', 'ASM', 55, '2007-12-11'),
    ('SE', 'ASM', 39, '2007-5-15'),
    ('SR', 'SEN', 35, '2006-6-6'),
    ('SE', 'SEN', 35, '2006-4-11'),
    ('SE', NULL, NULL, '2005-11-8'),
    ('SE', 'ASM', 53, '2005-9-13'),
    ('SE', 'GOV', NULL, '2003-10-7'),
    ('SE', 'ASM', 49, '2001-5-15'),
    ('SE', 'SEN', 24, '2001-3-26'),
    ('SR', 'ASM', 65, '2001-2-6'),
    ('SE', 'ASM', 65, '2001-4-3');
