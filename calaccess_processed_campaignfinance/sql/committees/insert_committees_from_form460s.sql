-- Insert any OCD Committee with a filer_id not already in CommitteeIdentifier.
INSERT INTO opencivicdata_committee (
    id,
    name,
    image,
    committee_type_id,
    created_at,
    updated_at,
    extras,
    locked_fields
)
SELECT 
    'ocd-campaign-finance-committee/' || gen_random_uuid() as id,
    f460.filer_lastname as name,
    '' as image,
    types.id as committee_type_id,
    now() as created_at,
    now() as updated_at,
    -- temporarily store the filer_id in the extras field
    -- this is removed in remove_calaccess_filer_ids_from_committees.sql
    jsonb_build_object('calaccess_filer_id', f460.filer_id) as extras,
    ARRAY[]::char[] as locked_fields
FROM calaccess_processed_form460filing f460
-- get the most recent filing of each filer
JOIN (
    SELECT filer_id, MAX(filing_id) as filing_id
    FROM calaccess_processed_form460filing
    GROUP BY 1
    -- filter out any filers already assigned an ocd-committee-id
    HAVING filer_id NOT IN (
        SELECT identifier::int as filer_id
        FROM opencivicdata_committeeidentifier
        WHERE scheme = 'calaccess_filer_id'
    )
) latest
ON f460.filing_id = latest.filing_id
-- TODO: figure out how to apply more specific CommitteeTypes (e.g., 'Candidate', 'Ballot Measure')
JOIN opencivicdata_committeetype types
ON types.name = 'Recipient';
