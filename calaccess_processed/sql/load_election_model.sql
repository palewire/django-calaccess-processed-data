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
UPDATE calaccess_processed_election as elec
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
