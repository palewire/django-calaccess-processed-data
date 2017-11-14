-- Insert missing FilingActionSummaryAmount records
INSERT INTO opencivicdata_filingactionsummaryamount (
    filing_action_id,
    label,
    amount_value,
    amount_currency
)
SELECT 
    fa.id as filing_action_id,
    %(label)s as label,
    COALESCE({source_table}.{source_column}, 0) as amount_value,
    'USD' as amount_currency
FROM {source_table}
-- (if inserting form a schedule summary table)
JOIN calaccess_processed_form460filingversion
ON {source_table}.filing_version_id = calaccess_processed_form460filingversion.id
JOIN opencivicdata_filingidentifier fi
ON calaccess_processed_form460filingversion.filing_id = fi.identifier::int
AND fi.scheme = 'calaccess_filing_id'
-- get the filing_action_id
JOIN opencivicdata_filingaction fa
ON fi.filing_id = fa.filing_id
AND calaccess_processed_form460filingversion.amend_id = (fa.extras->>'amend_id')::int
-- filter out summaries already inserted
LEFT JOIN opencivicdata_filingactionsummaryamount fasa
ON fa.id = fasa.filing_action_id
AND fasa.label = %(label)s
WHERE fasa.filing_action_id IS NULL;
