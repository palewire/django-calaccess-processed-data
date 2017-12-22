-- Insert any new Filing from Form460Filing
INSERT INTO opencivicdata_filing (
    id,
    classification,
    coverage_start_date,
    coverage_end_date,
    filer_id,
    recipient_id,
    created_at,
    updated_at,
    extras,
    locked_fields
)
SELECT
    'ocd-campaign-finance-filing/' || gen_random_uuid() as id, 
    'Form 460' as classification,
    f460.from_date as coverage_start_date,
    f460.thru_date as coverage_end_date,
    ci.committee_id as filer_id,
    o.id as recipient_id,
    now() as created_at,
    now() as updated_at,
    -- temporarily store the filer_id in the extras field
    -- this is removed in remove_calaccess_filer_ids_from_committees.sql
    jsonb_build_object('calaccess_filing_id', f460.filing_id) as extras,
    ARRAY[]::char[] as locked_fields
FROM calaccess_processed_form460filing f460
JOIN opencivicdata_committeeidentifier ci
ON f460.filer_id = ci.identifier::int
JOIN opencivicdata_organization o
ON o.name = 'California Secretary of State'
WHERE f460.filing_id NOT IN (
    SELECT identifier::int as filing_id
    FROM opencivicdata_filingidentifier
    WHERE scheme = 'calaccess_filing_id'
);