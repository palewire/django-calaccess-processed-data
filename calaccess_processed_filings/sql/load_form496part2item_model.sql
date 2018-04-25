INSERT INTO calaccess_processed_filings_form496part2item (
    filing_id,
    line_item,
    expense_date,
    amount,
    transaction_id,
    payment_description,
    memo_code,
    memo_reference_number
)
SELECT
    filing.filing_id,
    item_version.line_item,
    item_version.expense_date,
    item_version.amount,
    item_version.transaction_id,
    item_version.payment_description,
    item_version.memo_code,
    item_version.memo_reference_number
FROM calaccess_processed_filings_form496filing filing
JOIN calaccess_processed_filings_form496filingversion filing_version
ON filing.filing_id = filing_version.filing_id
AND filing.amendment_count = filing_version.amend_id
JOIN calaccess_processed_filings_form496part2itemversion item_version
ON filing_version.id = item_version.filing_version_id;
