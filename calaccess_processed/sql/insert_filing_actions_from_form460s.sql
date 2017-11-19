-- Insert any Form460FilingVersion as a FilingAction 
-- if filing_id/amend_id combo not in already in table
INSERT INTO opencivicdata_filingaction (
    id,
    filing_id,
    classification,
    description,
    date,
    supersedes_prior_versions,
    is_current,
    created_at,
    updated_at,
    extras,
    locked_fields
)
SELECT 
    'campaign-finance-filing-action/' || gen_random_uuid() as id,
    fi.filing_id as filing_id,
    CASE 
        WHEN f460v.amend_id = 0 THEN ARRAY['initial']
        ELSE ARRAY['amendment']
    END as classification,
    statement_type as description,
    date_filed as date,
    true as supersedes_prior_versions,
    f460v.amend_id = latest.amend_id as is_current,
    now() as created_at,
    now() as updated_at,
    jsonb_build_object('amend_id', f460v.amend_id) as extras,
    ARRAY[]::char[] as locked_fields
FROM calaccess_processed_form460filingversion f460v
-- get the filing_id
JOIN opencivicdata_filingidentifier fi
ON f460v.filing_id = fi.identifier::int
AND fi.scheme = 'calaccess_filing_id'
-- get the latest amend_id
JOIN (
    SELECT filing_id, MAX(amend_id) as amend_id
    FROM calaccess_processed_form460filingversion
    GROUP BY 1
) as latest
ON f460v.filing_id = latest.filing_id
-- filter out filing amendments already inserted
LEFT JOIN opencivicdata_filingaction fa
ON fi.filing_id = fa.filing_id
AND f460v.amend_id = (fa.extras->>'amend_id')::int
WHERE fa.filing_id IS NULL;
