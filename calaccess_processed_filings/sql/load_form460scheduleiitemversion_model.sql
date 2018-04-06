INSERT INTO calaccess_processed_filings_form460scheduleiitemversion (
    filing_version_id,
    line_item,
    date_received,
    date_received_thru,
    transaction_type,
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
    contributor_is_self_employed,
    intermediary_committee_id,
    intermediary_title,
    intermediary_lastname,
    intermediary_firstname,
    intermediary_name_suffix,
    intermediary_city,
    intermediary_state,
    intermediary_zip,
    intermediary_employer,
    intermediary_occupation,
    intermediary_is_self_employed,
    amount,
    receipt_description,
    cumulative_ytd_amount,
    cumulative_election_amount
)
SELECT
    filing_version.id AS filing_version_id,
    rcpt."LINE_ITEM" AS line_item,
    rcpt."RCPT_DATE" AS date_received,
    rcpt."DATE_THRU" AS date_received_thru,
    CASE
        WHEN UPPER(rcpt."TRAN_TYPE") = 'F' THEN 'Forgiven Loan'
        WHEN UPPER(rcpt."TRAN_TYPE") = 'I' THEN 'Intermediary'
        WHEN UPPER(rcpt."TRAN_TYPE") = 'R' THEN 'Returned'
        WHEN UPPER(rcpt."TRAN_TYPE") = 'T' THEN 'Third Party Repayment'
        WHEN UPPER(rcpt."TRAN_TYPE") = 'X' THEN 'Transfer'
        ELSE ''
    END AS transaction_type,
    rcpt."TRAN_ID" AS transaction_id,
    rcpt."MEMO_REFNO" AS memo_reference_number,
    CASE rcpt."ENTITY_CD"
        WHEN '0' THEN ''
        ELSE UPPER(rcpt."ENTITY_CD")
    END AS contributor_code,
    -- remove substrings like 'ID', 'I.D.', 'IC:', then remove '#'
    -- then trim leading/trailing whitespace
    -- btw...still a lot of cruft in this column
    TRIM(
        REPLACE(
            REGEXP_REPLACE(
                UPPER("CMTE_ID"),
                'I\.?[CD]\.?:?',
                ''
            ),
            '#',
            ''
        )
    ) AS contributor_committee_id,
    UPPER(rcpt."CTRIB_NAMT") AS contributor_title,
    UPPER(rcpt."CTRIB_NAML") AS contributor_lastname,
    UPPER(rcpt."CTRIB_NAMF") AS contributor_firstname,
    UPPER(rcpt."CTRIB_NAMS") AS contributor_name_suffix,
    UPPER(rcpt."CTRIB_CITY") AS contributor_city,
    UPPER(rcpt."CTRIB_ST") AS contributor_state,
    UPPER(rcpt."CTRIB_ZIP4") AS contributor_zip,
    UPPER(rcpt."CTRIB_EMP") AS contributor_employer,
    UPPER(rcpt."CTRIB_OCC") AS contributor_occupation,
    CASE UPPER(rcpt."CTRIB_SELF")
        WHEN 'Y' THEN true
        WHEN 'X' THEN true
        ELSE false
    END AS contributor_is_self_employed,
    TRIM(rcpt."INTR_CMTEID") AS intermediary_committee_id,
    UPPER(rcpt."INTR_NAMT") AS intermediary_title,
    UPPER(rcpt."INTR_NAML") AS intermediary_lastname,
    UPPER(rcpt."INTR_NAMF") AS intermediary_firstname,
    UPPER(rcpt."INTR_NAMS") AS intermediary_name_suffix,
    UPPER(rcpt."INTR_CITY") AS intermediary_city,
    UPPER(rcpt."INTR_ST") AS intermediary_state,
    UPPER(rcpt."INTR_ZIP4") AS intermediary_zip,
    UPPER(rcpt."INTR_EMP") AS intermediary_employer,
    UPPER(rcpt."INTR_OCC") AS intermediary_occupation,
    CASE UPPER(rcpt."INTR_SELF")
        WHEN 'Y' THEN true
        WHEN 'X' THEN true
        ELSE false
    END AS intermediary_is_self_employed,
    -- make sure all "returned" contributions are negative
    CASE
        WHEN rcpt."AMOUNT" > 0 AND UPPER(rcpt."TRAN_TYPE") = 'R'
            THEN 0 - rcpt."AMOUNT"
        ELSE
            rcpt."AMOUNT"
    END AS amount,
    rcpt."CTRIB_DSCR" AS receipt_description,
    rcpt."CUM_YTD" AS cumulative_ytd_amount,
    rcpt."CUM_OTH" AS cumulative_election_amount
FROM "RCPT_CD" rcpt
JOIN calaccess_processed_filings_form460filingversion filing_version
ON rcpt."FILING_ID" = filing_version.filing_id
AND rcpt."AMEND_ID" = filing_version.amend_id
WHERE rcpt."FORM_TYPE" = 'I';
