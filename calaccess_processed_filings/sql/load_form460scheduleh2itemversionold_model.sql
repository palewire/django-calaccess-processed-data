INSERT INTO calaccess_processed_filings_form460scheduleh2itemversionold (
    filing_version_id,
    line_item,
    date_repaid_or_forgiven,
    date_of_original_loan,
    recipient_code,
    recipient_committee_id,
    recipient_title,
    recipient_lastname,
    recipient_firstname,
    recipient_name_suffix,
    recipient_city,
    recipient_state,
    recipient_zip,
    recipient_employer,
    recipient_occupation,
    recipient_is_self_employed,
    intermediary_title,
    intermediary_lastname,
    intermediary_firstname,
    intermediary_name_suffix,
    intermediary_city,
    intermediary_state,
    intermediary_zip,
    treasurer_title,
    treasurer_lastname,
    treasurer_firstname,
    treasurer_name_suffix,
    treasurer_city,
    treasurer_state,
    treasurer_zip,
    interest_rate,
    repayment_type,
    amount_repaid_or_forgiven,
    outstanding_principle,
    transaction_id,
    memo_reference_number
)
SELECT
    filing_version.id AS filing_version_id,
    loan."LINE_ITEM" AS line_item,
    loan."LOAN_DATE2" AS date_repaid_or_forgiven,
    loan."LOAN_DATE1" AS date_of_original_loan,
    UPPER(loan."ENTITY_CD") as recipient_code,
    TRIM(
        REPLACE(
            REGEXP_REPLACE(
                UPPER(loan."CMTE_ID"),
                'I\.?[CD]\.?:?',
                ''
            ),
            '#',
            ''
        )
    ) AS recipient_committee_id,
    UPPER(loan."LNDR_NAMT") AS recipient_title,
    UPPER(loan."LNDR_NAML") AS recipient_lastname,
    UPPER(loan."LNDR_NAMF") AS recipient_firstname,
    UPPER(loan."LNDR_NAMS") AS recipient_name_suffix,
    UPPER(loan."LOAN_CITY") AS recipient_city,
    UPPER(loan."LOAN_ST") AS recipient_state,
    UPPER(loan."LOAN_ZIP4") AS recipient_zip,
    UPPER(loan."LOAN_EMP") AS recipient_employer,
    UPPER(loan."LOAN_OCC") AS recipient_occupation,
    CASE UPPER(loan."LOAN_SELF")
        WHEN 'Y' THEN true
        WHEN 'X' THEN true
        ELSE false
    END AS recipient_is_self_employed,
    UPPER(loan."INTR_NAMT") AS intermediary_title,
    UPPER(loan."INTR_NAML") AS intermediary_lastname,
    UPPER(loan."INTR_NAMF") AS intermediary_firstname,
    UPPER(loan."INTR_NAMS") AS intermediary_name_suffix,
    UPPER(loan."INTR_CITY") AS intermediary_city,
    UPPER(loan."INTR_ST") AS intermediary_state,
    UPPER(loan."INTR_ZIP4") AS intermediary_zip,
    UPPER(loan."TRES_NAMT") AS treasurer_title,
    UPPER(loan."TRES_NAML") AS treasurer_lastname,
    UPPER(loan."TRES_NAMF") AS treasurer_firstname,
    UPPER(loan."TRES_NAMS") AS treasurer_name_suffix,
    UPPER(loan."TRES_CITY") AS treasurer_city,
    UPPER(loan."TRES_ST") AS treasurer_state,
    UPPER(loan."TRES_ZIP4") AS treasurer_zip,
    loan."LOAN_RATE" AS interest_rate,
    loan."LOAN_TYPE" AS repayment_type,
    loan."LOAN_AMT1" AS amount_repaid_or_forgiven,
    loan."LOAN_AMT2" AS outstanding_principle,
    loan."TRAN_ID" AS transaction_id,
    loan."MEMO_REFNO" AS memo_reference_number
FROM "LOAN_CD" loan
JOIN calaccess_processed_filings_form460filingversion filing_version
ON loan."FILING_ID" = filing_version.filing_id
AND loan."AMEND_ID" = filing_version.amend_id
WHERE loan."FORM_TYPE" = 'H2';
