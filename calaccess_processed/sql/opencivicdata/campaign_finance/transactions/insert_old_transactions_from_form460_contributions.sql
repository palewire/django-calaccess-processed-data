-- Insert Transactions from Form460 contribution schedule item versions
INSERT INTO opencivicdata_transaction (
    id,    
    filing_action_id,
    classification,
    amount_value,
    amount_currency,
    is_in_kind,
    date,
    election_id,
    recipient_entity_type,
    recipient_committee_id,
    recipient_organization_id,
    recipient_person_id,
    sender_entity_type,
    sender_committee_id,
    sender_organization_id,
    sender_person_id,
    created_at,
    updated_at,
    locked_fields,
    extras
)
SELECT
    'campaign-finance-filing-transaction/' || gen_random_uuid() as id, 
    fa.id as filing_action_id,
    item.transaction_type as classification,
    item.{source_amount_column} as amount_value,
    'USD' as amount_currency,
    %(is_in_kind)s as is_in_kind,
    date_received as date,
    e.id as election_id,
    'committee' as recipient_entity_type,
    f.filer_id as recipient_committee_id,
    NULL as recipient_organization_id,
    NULL as recipient_person_id,
    CASE
        WHEN item.contributor_code = 'COM' THEN 'committee'
        WHEN item.contributor_code = 'SCC' THEN 'committee'
        WHEN item.contributor_code = 'RCP' THEN 'committee'
        WHEN item.contributor_code = 'PTY' THEN 'organization'
        WHEN item.contributor_code = 'OTH' THEN 'organization'        
        WHEN item.contributor_code = 'IND' THEN 'person'
        WHEN item.contributor_code = 'OFF' THEN 'person'
        ELSE 'unknown'
    END as sender_entity_type,
    NULL as sender_committee_id,
    NULL as sender_organization_id,
    NULL as sender_person_id,
    now() as created_at,
    now() as updated_at,
    ARRAY[]::char[] as locked_fields,
    jsonb_build_object('transaction_id', item.transaction_id) ||
    jsonb_build_object('line_number', item.line_item) as extras
FROM {source_table} item
-- join to Form460FilingVersion
JOIN calaccess_processed_form460filingversion fv
ON item.filing_version_id = fv.id
-- so that we can join to FilingIdentifier on calaccess filing_id
JOIN opencivicdata_filingidentifier fi
ON fv.filing_id = identifier::int
AND fi.scheme = 'calaccess_filing_id'
-- to get the ocd filing_id
-- so that we can join to FilingAction ocd filing_id and calaccess_amend_id
JOIN opencivicdata_filingaction fa
ON fi.filing_id = fa.filing_id
AND fv.amend_id = (fa.extras->>'amend_id')::int
AND fa.is_current = false
-- and join to ocd Filing to get the filer_id
JOIN opencivicdata_filing f
ON fa.filing_id = f.id
-- and join to OCD Election so that we can get the ocd_election_id
LEFT JOIN opencivicdata_election e
ON fv.election_date = e.date
-- filter out transactions already inserted
-- get the distinct filing_action_ids of transactions already inserted
LEFT JOIN (
    SELECT DISTINCT filing_action_id
    FROM opencivicdata_transaction
    WHERE is_in_kind = %(is_in_kind)s
) t
ON fa.id = t.filing_action_id
WHERE t.filing_action_id IS NULL;
-- LEFT JOIN opencivicdata_transaction t
-- ON fa.id = t.filing_action_id
-- AND item.line_item = (t.extras->>'line_number')::int
-- WHERE t.filing_action_id IS NULL;
