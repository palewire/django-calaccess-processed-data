-- Updating target field on any existing Filing from source table and column
UPDATE opencivicdata_filing
SET 
    {target_column} = {source_table}.{source_column},
    updated_at = now()
FROM opencivicdata_filing f
-- join to FilingIdentifier to get calaccess_filing_id 
JOIN opencivicdata_filingidentifier fi
ON f.id = fi.filing_id
AND fi.scheme = 'calaccess_filing_id'
-- then join to source_table
JOIN {source_table}
ON {source_table}.filing_id = fi.identifier::int
-- filter down to only values that need to be updated
WHERE f.{target_column} <> {source_table}.{source_column};
