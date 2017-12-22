INSERT INTO calaccess_processed_form460scheduleb2itemversion (
    filing_version_id,
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
    filing_version.id AS filing_version_id,
    loan."LINE_ITEM" AS line_item,
    UPPER(loan."ENTITY_CD") as guarantor_code,
    UPPER(loan."LNDR_NAMT") AS guarantor_title,
    UPPER(loan."LNDR_NAML") AS guarantor_lastname,
    UPPER(loan."LNDR_NAMF") AS guarantor_firstname,
    UPPER(loan."LNDR_NAMS") AS guarantor_name_suffix,
    UPPER(loan."LOAN_CITY") AS guarantor_city,
    UPPER(loan."LOAN_ST") AS guarantor_state,
    UPPER(loan."LOAN_ZIP4") AS guarantor_zip,
    UPPER(loan."LOAN_EMP") AS guarantor_employer,
    UPPER(loan."LOAN_OCC") AS guarantor_occupation,
    CASE UPPER(loan."LOAN_SELF")
        WHEN 'Y' THEN true
        WHEN 'X' THEN true
        ELSE false 
    END AS guarantor_is_self_employed,
    UPPER(loan."INTR_NAML") AS lender_name,
    loan."LOAN_AMT1" AS amount_guaranteed_this_period,
    loan."LOAN_AMT2" AS balance_outstanding_to_date,
    loan."LOAN_AMT3" AS cumulative_ytd_amount,
    loan."LOAN_DATE1" AS loan_date,
    loan."LOAN_RATE" AS interest_rate,
    loan."TRAN_ID" AS transaction_id,
    loan."MEMO_REFNO" AS memo_reference_number,
    false as reported_on_b1
FROM "LOAN_CD" loan
JOIN calaccess_processed_form460filingversion filing_version
ON loan."FILING_ID" = filing_version.filing_id
AND loan."AMEND_ID" = filing_version.amend_id
WHERE loan."FORM_TYPE" = 'B2'
AND loan."LOAN_TYPE" = ''
AND loan."LOAN_DATE1" >= '2000-12-22'
-- Also include loan guarantor items from the older version
-- of Schedule B, Part 1
UNION
SELECT
    filing_version.id AS filing_version_id,
    loan."LINE_ITEM" AS line_item,
    UPPER(loan."ENTITY_CD") as guarantor_code,
    UPPER(loan."LNDR_NAMT") AS guarantor_title,
    UPPER(loan."LNDR_NAML") AS guarantor_lastname,
    UPPER(loan."LNDR_NAMF") AS guarantor_firstname,
    UPPER(loan."LNDR_NAMS") AS guarantor_name_suffix,
    UPPER(loan."LOAN_CITY") AS guarantor_city,
    UPPER(loan."LOAN_ST") AS guarantor_state,
    UPPER(loan."LOAN_ZIP4") AS guarantor_zip,
    UPPER(loan."LOAN_EMP") AS guarantor_employer,
    UPPER(loan."LOAN_OCC") AS guarantor_occupation,
    CASE UPPER(loan."LOAN_SELF")
        WHEN 'Y' THEN true
        WHEN 'X' THEN true
        ELSE false 
    END AS guarantor_is_self_employed,
    UPPER(loan."INTR_NAML") AS lender_name,
    loan."LOAN_AMT1" AS amount_guaranteed_this_period,
    loan."LOAN_AMT2" AS balance_outstanding_to_date,
    loan."LOAN_AMT3" AS cumulative_ytd_amount,
    loan."LOAN_DATE1" AS loan_date,
    loan."LOAN_RATE" AS interest_rate,
    loan."TRAN_ID" AS transaction_id,
    loan."MEMO_REFNO" AS memo_reference_number,
    true as reported_on_b1
FROM "LOAN_CD" loan
JOIN calaccess_processed_form460filingversion filing_version
ON loan."FILING_ID" = filing_version.filing_id
AND loan."AMEND_ID" = filing_version.amend_id
WHERE loan."FORM_TYPE" = 'B1'
AND loan."LOAN_TYPE" = 'B1G';