INSERT INTO calaccess_processed_candidatecommittee (
        candidate_filer_id,
        committee_filer_id,
        link_type_id,
        link_type_description,
        first_session,
        last_session,
        first_effective_date,
        last_effective_date,
        first_termination_date,
        last_termination_date
)        
SELECT   
        candidate_filer_id,
        committee_filer_id,
        @link_type AS link_type_id,
        lu."CODE_DESC" AS link_type_description,
        MIN(session) AS first_session,
        MAX(session) AS last_session,
        MIN(effective_date) AS first_effective_date,
        MAX(effective_date) AS last_effective_date,
        MIN(termination_date) AS first_termination_date,
        MAX(termination_date) AS last_termination_date
FROM (
        -- select all FILER_LINKS_CD records where FILER_A was ever a candidate
        SELECT 
                links."FILER_ID_A" AS candidate_filer_id,
                links."FILER_ID_B" AS committee_filer_id,
                "LINK_TYPE" AS link_type,
                CASE "SESSION_ID" 
                        WHEN 0 THEN NULL
                        ELSE "SESSION_ID"
                END AS session,
                "ACTIVE_FLG" AS active,
                "EFFECT_DT" AS effective_date,
                "TERMINATION_DT" AS termination_date
        FROM "FILER_LINKS_CD" links
        JOIN (
                SELECT DISTINCT "FILER_ID"
                FROM "FILER_TO_FILER_TYPE_CD"
                WHERE "FILER_TYPE" = 8
        ) cands
        ON cands."FILER_ID" = links."FILER_ID_A"
        -- and FILER_B was ever a recipient committee
        JOIN (
                SELECT DISTINCT "FILER_ID"
                FROM "FILER_TO_FILER_TYPE_CD"
                WHERE "FILER_TYPE" = 16
        ) comms
        ON comms."FILER_ID" = links."FILER_ID_B"
        -- union with all LINK records where FILER B was ever a candidate
        UNION ALL
        SELECT 
                links."FILER_ID_B" AS candidate_filer_id,
                links."FILER_ID_A" AS committee_filer_id,
                "LINK_TYPE" as link_type,
                CASE "SESSION_ID" 
                        WHEN 0 THEN NULL
                        ELSE "SESSION_ID"
                END AS session,
                "ACTIVE_FLG" AS active,
                "EFFECT_DT" AS effective_date,
                "TERMINATION_DT" AS termination_date
        FROM "FILER_LINKS_CD" links
        JOIN (
                SELECT DISTINCT "FILER_ID"
                FROM "FILER_TO_FILER_TYPE_CD"
                WHERE "FILER_TYPE" = 8
        ) cands
        ON cands."FILER_ID" = links."FILER_ID_B"
        -- and FILER_A was ever a recipient committee
        JOIN (
                SELECT DISTINCT "FILER_ID"
                FROM "FILER_TO_FILER_TYPE_CD"
                WHERE "FILER_TYPE" = 16
        ) comms
        ON comms."FILER_ID" = links."FILER_ID_A"
) as all_links
JOIN "LOOKUP_CODES_CD" lu
ON @link_type = lu."CODE_ID"
AND lu."CODE_TYPE" = 12000
GROUP BY 1, 2, 3, 4;