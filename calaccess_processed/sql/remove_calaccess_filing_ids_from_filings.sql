-- Remove the 'calaccess_filer_id' value from the "extras" field on Committees.
UPDATE opencivicdata_filing
SET extras = extras - 'calaccess_filing_id'
WHERE extras ? 'calaccess_filing_id';
