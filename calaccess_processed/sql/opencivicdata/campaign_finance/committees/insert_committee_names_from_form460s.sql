-- Inserting missing alternate Committee Names from Form460FilingVersions
INSERT INTO opencivicdata_committeename (
    id,
    name,
    note,
    start_date,
    end_date,
    committee_id
)
SELECT
    gen_random_uuid() as id,
    f460.filer_lastname as name,
    'From Form460Filing ' || f460.filing_id as note,
    '' as start_date,
    '' as end_date,
    ci.committee_id as committee_id
-- get every filer_id/filer_lastname combo (and latest filing_id)
FROM (
    SELECT filer_id, filer_lastname, MAX(filing_id) as filing_id
    FROM calaccess_processed_form460filingversion
    GROUP BY 1, 2
) f460
JOIN opencivicdata_committeeidentifier ci
ON ci.identifier::int = f460.filer_id
-- filter out ocd-committee-id/name combos already inserted
LEFT JOIN opencivicdata_committeename cn
ON ci.committee_id = cn.committee_id
AND f460.filer_lastname = cn.name
WHERE cn.committee_id IS NULL;