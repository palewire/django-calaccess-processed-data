-- Insert any OCD Committee with a filer_id not already in CommitteeIdentifier.
INSERT INTO opencivicdata_committeeidentifier (
    id,
    scheme,
    committee_id,
    identifier
)
SELECT 
    gen_random_uuid() as id,
    'calaccess_filer_id' as scheme,
    id as committee_id, 
    extras->>'calaccess_filer_id' as identifier
FROM opencivicdata_committee
WHERE extras ? 'calaccess_filer_id';
