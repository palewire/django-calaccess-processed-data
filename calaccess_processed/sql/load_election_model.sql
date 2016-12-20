INSERT INTO calaccess_processed_election (
            year,
            election_type,
            office,
            district,
            election_date
        )        
SELECT 
        -- extract the four-digit year, cast as an int
        substring(cand.name from '\d{4}')::INT AS year,
        CASE 
            WHEN cand.name LIKE '%PRIMARY%' THEN 'P'
            WHEN cand.name LIKE '%GENERAL%' THEN 'G'
            WHEN cand.name LIKE '%RECALL%' THEN 'R'
            WHEN cand.name LIKE '%SPECIAL ELECTION%' THEN 'SE'
            WHEN cand.name LIKE '%SPECIAL RUNOFF%' THEN 'SR'
        END AS election_type,
        CASE
            WHEN cand.name LIKE '%ASSEMBLY%' THEN 'ASM'
            WHEN cand.name LIKE '%STATE SENATE%' THEN 'SEN'
            WHEN cand.name LIKE '%GOVERNOR%' THEN 'GOV'
            ELSE NULL
        END AS office,
        -- extract the two digit chars found in the parenthesis, if any
        substring(cand.name from '^\d{4}\s.+\(.+(\d{2})\)$')::INT AS district,
        -- this field is populate by the update statement below
        NULL as election_date
  FROM calaccess_processed_candidatescrapedelection AS cand;

-- hardcode this election date because for some reason the CAL-ACCESS ballot props
-- page has two "primaries" for 2008
UPDATE calaccess_processed_election
   SET election_date = '2008-2-5'
 WHERE election_type = 'P'
   AND year = 2008;

-- there was only one special election the years 2003 and 2005
UPDATE calaccess_processed_election AS elec
   SET election_date = prop.election_date
  FROM (
        SELECT substring(name from '\d{4}')::INT AS year,
               substring(name from '\d{4}\s([A-Z])') AS election_type,
               (regexp_matches(name, '^([A-Z]+\s\d{1,2},\s\d{4})\s.+$'))[1]::DATE AS election_date
          FROM calaccess_processed_propositionscrapedelection
         WHERE name LIKE '%2003%' 
            OR name LIKE '%2005%'
       ) AS prop
 WHERE elec.year = prop.year
   AND elec.election_type = 'SE';

-- these all come from here: http://www.sos.ca.gov/elections/prior-elections/special-elections/
UPDATE calaccess_processed_election
   SET election_date = '2016-4-5'
 WHERE year = 2016
   AND election_type = 'SE'
   AND office = 'ASM'
   AND district = 31;

UPDATE calaccess_processed_election
   SET election_date = '2015-3-17'
 WHERE year = 2015
   AND election_type = 'SE'
   AND office = 'SEN'
   AND district = 37;

UPDATE calaccess_processed_election
   SET election_date = '2015-3-17'
 WHERE year = 2015
   AND election_type = 'SE'
   AND office = 'SEN'
   AND district = 21;

UPDATE calaccess_processed_election
   SET election_date = '2014-3-25'
 WHERE year = 2014
   AND election_type = 'SE'
   AND office = 'SEN'
   AND district = 23;

UPDATE calaccess_processed_election
   SET election_date = '2014-12-9'
 WHERE year = 2014
   AND election_type = 'SE'
   AND office = 'SEN'
   AND district = 35;

UPDATE calaccess_processed_election
   SET election_date = '2013-12-3'
 WHERE year = 2014
   AND election_type = 'SE'
   AND office = 'ASM'
   AND district = 54;

UPDATE calaccess_processed_election
   SET election_date = '2013-9-17'
 WHERE year = 2013
   AND election_type = 'SE'
   AND office = 'SEN'
   AND district = 26;

UPDATE calaccess_processed_election
   SET election_date = '2013-5-21'
 WHERE year = 2013
   AND election_type = 'SE'
   AND office = 'ASM'
   AND district = 80;

UPDATE calaccess_processed_election
   SET election_date = '2013-3-12'
 WHERE year = 2013
   AND election_type = 'SE'
   AND office = 'SEN'
   AND district = 40;

UPDATE calaccess_processed_election
   SET election_date = '2013-1-8'
 WHERE year = 2013
   AND election_type = 'SE'
   AND office = 'SEN'
   AND district = 4;

UPDATE calaccess_processed_election
   SET election_date = '2012-11-6'
 WHERE year = 2012
   AND election_type = 'SE'
   AND office = 'SEN'
   AND district = 4;

UPDATE calaccess_processed_election
   SET election_date = '2011-2-15'
 WHERE year = 2011
   AND election_type = 'SE'
   AND office = 'SEN'
   AND district = 17;

UPDATE calaccess_processed_election
   SET election_date = '2011-2-15'
 WHERE year = 2011
   AND election_type = 'SE'
   AND office = 'SEN'
   AND district = 28;

UPDATE calaccess_processed_election
   SET election_date = '2011-1-4'
 WHERE year = 2011
   AND election_type = 'SR'
   AND office = 'SEN'
   AND district = 1;

UPDATE calaccess_processed_election
   SET election_date = '2010-1-12'
 WHERE year = 2010
   AND election_type = 'SR'
   AND office = 'ASM'
   AND district = 72;

UPDATE calaccess_processed_election
   SET election_date = '2010-11-2'
 WHERE year = 2010
   AND election_type = 'SE'
   AND office = 'SEN'
   AND district = 1;

UPDATE calaccess_processed_election
   SET election_date = '2009-9-1'
 WHERE year = 2009
   AND election_type = 'SE'
   AND office = 'ASM'
   AND district = 51;

UPDATE calaccess_processed_election
   SET election_date = '2009-11-17'
 WHERE year = 2009
   AND election_type = 'SE'
   AND office = 'ASM'
   AND district = 72;

UPDATE calaccess_processed_election
   SET election_date = '2008-2-5'
 WHERE year = 2008
   AND election_type = 'SR'
   AND office = 'ASM'
   AND district = 55;

UPDATE calaccess_processed_election
   SET election_date = '2007-5-15'
 WHERE year = 2007
   AND election_type = 'SE'
   AND office = 'ASM'
   AND district = 39;

UPDATE calaccess_processed_election
   SET election_date = '2007-12-11'
 WHERE year = 2007
   AND election_type = 'SE'
   AND office = 'ASM'
   AND district = 55;


-- then populate the election_date field for prop elections that match cand elections
UPDATE calaccess_processed_election as elec
   SET election_date = (regexp_matches(prop.name, '^([A-Z]+\s\d{1,2},\s\d{4})\s.+$'))[1]::DATE
  FROM calaccess_processed_propositionscrapedelection AS prop
 WHERE elec.year = substring(name from '\d{4}')::INT
   AND elec.election_type = substring(name from '\d{4}\s([A-Z])')
   -- exclude special elections from match b/c we can't be sure these all
   -- occurred on the same date
   AND prop.name NOT LIKE '%SPECIAL%'
   AND elec.election_type NOT IN ('SE', 'SR')
   AND elec.election_date IS NULL;
