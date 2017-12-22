INSERT INTO calaccess_processed_form460scheduleb2item (
    filing_id,
    line_item,
    guarantor_code,
    guarantor_title,
    guarantor_lastname,
    guarantor_firstname,
    guarantor_name_suffix,
    guarantor_city,
    guarantor_state,
    guarantor_zip,
    guarantor_employer,
    guarantor_occupation,
    guarantor_is_self_employed,
    lender_name,
    amount_guaranteed_this_period,
    balance_outstanding_to_date,
    cumulative_ytd_amount,
    loan_date,
    interest_rate,
    transaction_id,
    memo_reference_number, 
    reported_on_b1
)
SELECT 
    filing_version.filing_id,
    item_version.line_item,
    item_version.guarantor_code,
    item_version.guarantor_title,
    item_version.guarantor_lastname,
    item_version.guarantor_firstname,
    item_version.guarantor_name_suffix,
    item_version.guarantor_city,
    item_version.guarantor_state,
    item_version.guarantor_zip,
    item_version.guarantor_employer,
    item_version.guarantor_occupation,
    item_version.guarantor_is_self_employed,
    item_version.lender_name,
    item_version.amount_guaranteed_this_period,
    item_version.balance_outstanding_to_date,
    item_version.cumulative_ytd_amount,
    item_version.loan_date,
    item_version.interest_rate,
    item_version.transaction_id,
    item_version.memo_reference_number, 
    item_version.reported_on_b1
FROM calaccess_processed_form460filing filing
JOIN calaccess_processed_form460filingversion filing_version
ON filing.filing_id = filing_version.filing_id
AND filing.amendment_count = filing_version.amend_id
JOIN calaccess_processed_form460scheduleb2itemversion item_version
ON filing_version.id = item_version.filing_version_id;