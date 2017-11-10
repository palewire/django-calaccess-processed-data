-- Updating name field on any existing Committee from Form460Filing
UPDATE opencivicdata_filing
SET {to_update} = {source_table}.{source_column}
FROM opencivicdata_filing f
-- join to FilingIdentifier to get calaccess_filing_id 
JOIN opencivicdata_filingidentifier fi
ON f.id = fi.filing_id
AND fi.scheme = 'calaccess_filing_id'
-- then join to Form460Filing
JOIN calaccess_processed_form460filing
ON calaccess_processed_form460filing.filing_id = fi.identifier::int
-- then join to CommitteeIdentifier to get OCD committee_id
JOIN opencivicdata_committeeidentifier
ON calaccess_processed_form460filing.filer_id = opencivicdata_committeeidentifier.identifier::int
AND opencivicdata_committeeidentifier.scheme = 'calaccess_filer_id'
-- this filter is very important
WHERE f.{to_update} <> {source_table}.{source_column};
