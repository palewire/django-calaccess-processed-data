-- Remove the 'calaccess_filer_id' value from the "extras" field on Committees.
UPDATE opencivicdata_committee
SET extras = extras - 'calaccess_filer_id'
WHERE extras ? 'calaccess_filer_id';
