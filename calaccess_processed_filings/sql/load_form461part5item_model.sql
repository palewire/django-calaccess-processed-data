INSERT INTO calaccess_processed_filings_form461part5item (
    filing_id,
    line_item,
    payee_code,
    payee_committee_id,
    payee_title,
    payee_lastname,
    payee_firstname,
    payee_name_suffix,
    payee_city,
    payee_state,
    payee_zip,
    treasurer_title,
    treasurer_lastname,
    treasurer_firstname,
    treasurer_name_suffix,
    treasurer_city,
    treasurer_state,
    treasurer_zip,
    payment_code,
    payment_description,
    amount,
    cumulative_ytd_amount,
    expense_date,
    check_number,
    transaction_id,
    memo_reference_number,
    support_oppose_code,
    ballot_measure_jurisdiction,
    ballot_measure_name,
    ballot_measure_num,
    candidate_district,
    candidate_jurisdiction_code,
    candidate_jurisdiction_description,
    candidate_title,
    candidate_firstname,
    candidate_lastname,
    candidate_name_suffix,
    office_code,
    office_description,
    office_sought_held
)
SELECT
    filing.filing_id,
    item_version.line_item,
    item_version.payee_code,
    item_version.payee_committee_id,
    item_version.payee_title,
    item_version.payee_lastname,
    item_version.payee_firstname,
    item_version.payee_name_suffix,
    item_version.payee_city,
    item_version.payee_state,
    item_version.payee_zip,
    item_version.treasurer_title,
    item_version.treasurer_lastname,
    item_version.treasurer_firstname,
    item_version.treasurer_name_suffix,
    item_version.treasurer_city,
    item_version.treasurer_state,
    item_version.treasurer_zip,
    item_version.payment_code,
    item_version.payment_description,
    item_version.amount,
    item_version.cumulative_ytd_amount,
    item_version.expense_date,
    item_version.check_number,
    item_version.transaction_id,
    item_version.memo_reference_number,
    item_version.support_oppose_code,
    item_version.ballot_measure_jurisdiction,
    item_version.ballot_measure_name,
    item_version.ballot_measure_num,
    item_version.candidate_district,
    item_version.candidate_jurisdiction_code,
    item_version.candidate_jurisdiction_description,
    item_version.candidate_title,
    item_version.candidate_firstname,
    item_version.candidate_lastname,
    item_version.candidate_name_suffix,
    item_version.office_code,
    item_version.office_description,
    item_version.office_sought_held
FROM calaccess_processed_filings_form461filing filing
JOIN calaccess_processed_filings_form461filingversion filing_version
ON filing.filing_id = filing_version.filing_id
AND filing.amendment_count = filing_version.amend_id
JOIN calaccess_processed_filings_form461part5itemversion item_version
ON filing_version.id = item_version.filing_version_id;
