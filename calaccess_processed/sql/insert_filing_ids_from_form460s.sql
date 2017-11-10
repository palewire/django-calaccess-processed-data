-- Insert any OCD Filing with a filing_id not already in FilingIdentifier.
INSERT INTO opencivicdata_filingidentifier (
    id,
    scheme,
    filing_id,
    identifier
)
SELECT 
    gen_random_uuid() as id,
    'calaccess_filing_id' as scheme,
    id as filing_id, 
    extras->>'calaccess_filing_id' as identifier
FROM opencivicdata_filing
WHERE extras ? 'calaccess_filing_id';
