-- Update filer_id on OCD Filing
UPDATE opencivicdata_filing
SET 
    filer_id = ci.committee_id,
    updated_at = now()
FROM opencivicdata_filing f
-- join to FilingIdentifier to get calaccess_filing_id 
JOIN opencivicdata_filingidentifier fi
ON f.id = fi.filing_id
AND fi.scheme = 'calaccess_filing_id'
-- then join to source_table
JOIN {processed_data_table}
ON {processed_data_table}.filing_id = fi.identifier::int
-- then to CommitteeIdentifier
JOIN opencivicdata_committeeidentifier ci
ON {processed_data_table}.filer_id = ci.identifier::int
AND ci.scheme = 'calaccess_filer_id'
-- filter down to only values that need to be updated
WHERE f.filer_id <> ci.committee_id;
