-- Updating name field on any existing Committee from Form460Filing
UPDATE opencivicdata_committee
SET 
    name = f460.filer_lastname,
    updated_at = now()
FROM opencivicdata_committee c
JOIN opencivicdata_committeeidentifier ci
ON c.id = ci.committee_id
AND ci.scheme = 'calaccess_filer_id'
-- filter down to most recent filings
JOIN (
    SELECT filer_id, MAX(filing_id) as filing_id
    FROM calaccess_processed_form460filing
    GROUP BY 1
) latest
ON ci.identifier::int = latest.filer_id
JOIN calaccess_processed_form460filing f460
ON f460.filing_id = latest.filing_id
WHERE c.name <> f460.filer_lastname;
