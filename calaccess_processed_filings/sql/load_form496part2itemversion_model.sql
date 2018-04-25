INSERT INTO calaccess_processed_filings_form496part2itemversion (
    filing_version_id,
    line_item,
    expense_date,
    amount,
    transaction_id,
    payment_description,
    memo_code,
    memo_reference_number
)
SELECT
    filing_version.id AS filing_version_id,
    s496_line."LINE_ITEM" AS line_item,
    s496_line."EXP_DATE" AS expense_date,
    s496_line."AMOUNT" AS amount,
    s496_line."TRAN_ID" AS transaction_id,
    s496_line."EXPN_DSCR" as payment_description,
    s496_line."MEMO_CODE" as memo_code,
    s496_line."MEMO_REFNO" AS memo_reference_number
FROM "S496_CD" s496_line
JOIN calaccess_processed_filings_form496filingversion filing_version
ON s496_line."FILING_ID" = filing_version.filing_id
AND s496_line."AMEND_ID" = filing_version.amend_id;
