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
            WHEN cand.name LIKE 'ASSEMBLY%' THEN 'ASM'
            WHEN cand.name LIKE 'STATE SENATE%' THEN 'SEN'
            WHEN cand.name LIKE 'GOVERNOR%' THEN 'GOV'
            ELSE NULL
        END AS office,
        -- extract the two digit chars found in the parenthesis, if any
        substring(cand.name from '^\d{4}\s.+\(.+(\d{2})\)$')::INT AS district,
        -- this field is populate by the update statement below
        NULL as election_date
  FROM calaccess_processed_candidatescrapedelection AS cand;

-- then populate the election_date field for prop elections that match cand elections
UPDATE calaccess_processed_election as elec
   SET election_date = prop.election_date
  FROM (
        SELECT
                substring(name from '\d{4}')::INT as year,
                CASE 
                    WHEN name LIKE '%PRIMARY' THEN 'P'
                    WHEN name LIKE '%GENERAL' THEN 'G'
                    WHEN name LIKE '%RECALL' THEN 'R'
                    ELSE NULL
                END AS election_type,
                (regexp_matches(name, '^([A-Z]+\s\d{1,2},\s\d{4})\s.+$'))[1]::DATE AS election_date
         FROM calaccess_processed_propositionscrapedelection
       ) as prop
 WHERE elec.year = prop.year
   AND elec.election_type = prop.election_type;

-- finally, insert any other prop elections we might be missing still