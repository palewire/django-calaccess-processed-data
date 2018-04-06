INSERT INTO calaccess_processed_filings_form497part1item (
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
    filing.filing_id,
    item_version.line_item,
    item_version.date_received,
    item_version.date_received_thru,
    item_version.amount_received,
    item_version.transaction_id,
    item_version.memo_reference_number,
    item_version.contributor_code,
    item_version.contributor_committee_id,
    item_version.contributor_title,
    item_version.contributor_lastname,
    item_version.contributor_firstname,
    item_version.contributor_name_suffix,
    item_version.contributor_city,
    item_version.contributor_state,
    item_version.contributor_zip,
    item_version.contributor_employer,
    item_version.contributor_occupation,
    item_version.contributor_is_self_employed
FROM calaccess_processed_filings_form497filing filing
JOIN calaccess_processed_filings_form497filingversion filing_version
ON filing.filing_id = filing_version.filing_id
AND filing.amendment_count = filing_version.amend_id
JOIN calaccess_processed_filings_form497part1itemversion item_version
ON filing_version.id = item_version.filing_version_id;
