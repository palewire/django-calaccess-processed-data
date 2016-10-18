INSERT INTO calaccess_processed_latecontributionreceived (
    filing_id,
    line_item,
    date_received,
    date_received_thru,
    amount_received,
    transaction_id,
    memo_reference_number,
    contributor_code,
    contributor_committee_id,
    contributor_title,
    contributor_lastname,
    contributor_firstname,
    contributor_name_suffix,
    contributor_city,
    contributor_state,
    contributor_zip,
    contributor_employer,
    contributor_occupation,
    contributor_is_self_employed
)
SELECT 
    contrib_version.filing_id,
    contrib_version.line_item,
    contrib_version.date_received,
    contrib_version.date_received_thru,
    contrib_version.amount_received,
    contrib_version.transaction_id,
    contrib_version.memo_reference_number,
    contrib_version.contributor_code,
    contrib_version.contributor_committee_id,
    contrib_version.contributor_title,
    contrib_version.contributor_lastname,
    contrib_version.contributor_firstname,
    contrib_version.contributor_name_suffix,
    contrib_version.contributor_city,
    contrib_version.contributor_state,
    contrib_version.contributor_zip,
    contrib_version.contributor_employer,
    contrib_version.contributor_occupation,
    contrib_version.contributor_is_self_employed
FROM calaccess_processed_latecontributionreceivedversion contrib_version
JOIN calaccess_processed_schedule497 filing
ON contrib_version.filing_id = filing.filing_id
AND contrib_version.amend_id = filing.amendment_count;