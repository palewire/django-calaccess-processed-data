INSERT INTO calaccess_processed_filings_form460filingversion (
    filing_id,
    amend_id,
    filer_id,
    date_filed,
    statement_type,
    from_date,
    thru_date,
    filer_lastname,
    filer_firstname,
    election_date,
    monetary_contributions,
    loans_received,
    subtotal_cash_contributions,
    nonmonetary_contributions,
    total_contributions,
    payments_made,
    loans_made,
    subtotal_cash_payments,
    unpaid_bills,
    nonmonetary_adjustment,
    total_expenditures_made,
    beginning_cash_balance,
    cash_receipts,
    miscellaneous_cash_increases,
    cash_payments,
    ending_cash_balance,
    loan_guarantees_received,
    cash_equivalents,
    outstanding_debts
)
SELECT
    cvr."FILING_ID" AS filing_id,
    cvr."AMEND_ID" AS amend_id,
    x."FILER_ID" AS filer_id,
    cvr."RPT_DATE" AS date_filed,
    CASE
        WHEN UPPER(cvr."STMT_TYPE") = 'PE' THEN 'Pre-Election'
        WHEN UPPER(cvr."STMT_TYPE") = 'QS' THEN 'Quarterly'
        WHEN UPPER(cvr."STMT_TYPE") = 'QT' THEN 'Quarterly'
        WHEN UPPER(cvr."STMT_TYPE") = 'SA' THEN 'Semi-Annual'
        WHEN UPPER(cvr."STMT_TYPE") = 'S1' THEN 'Semi-Annual'
        WHEN UPPER(cvr."STMT_TYPE") = 'S2' THEN 'Semi-Annual'
        WHEN UPPER(cvr."STMT_TYPE") = 'SE' THEN 'Supplemental Pre-elect'
        WHEN UPPER(cvr."STMT_TYPE") = 'SY' THEN 'Special Odd-Yr. Campaign'
        WHEN UPPER(cvr."STMT_TYPE") = 'TS' THEN 'Termination Statement'
        WHEN cvr."STMT_TYPE" = '**' THEN 'Amendment'
        ELSE 'Unknown'
    END AS statement_type,
    cvr."FROM_DATE" AS from_date,
    cvr."THRU_DATE" AS thru_date,
    UPPER(cvr."FILER_NAML") AS filer_lastname,
    CASE
        WHEN cvr."FILER_NAMF" IN ('.', '-') THEN ''
        ELSE UPPER(cvr."FILER_NAMF")
    END AS filer_firstname,
    cvr."ELECT_DATE" AS election_date,
    line_1."AMOUNT_A" AS monetary_contributions,
    line_2."AMOUNT_A" AS loans_received,
    line_3."AMOUNT_A" AS subtotal_cash_contributions,
    line_4."AMOUNT_A" AS nonmonetary_contributions,
    line_5."AMOUNT_A" AS total_contributions,
    line_6."AMOUNT_A" AS payments_made,
    line_7."AMOUNT_A" AS loans_made,
    line_8."AMOUNT_A" AS subtotal_cash_payments,
    line_9."AMOUNT_A" AS unpaid_bills,
    line_10."AMOUNT_A" AS nonmonetary_adjustment,
    line_11."AMOUNT_A" AS total_expenditures_made,
    line_12."AMOUNT_A" AS beginning_cash_balance,
    line_13."AMOUNT_A" AS cash_receipts,
    line_14."AMOUNT_A" AS miscellaneous_cash_increases,
    line_15."AMOUNT_A" AS cash_payments,
    line_16."AMOUNT_A" AS ending_cash_balance,
    line_17."AMOUNT_A" AS loan_guarantees_received,
    line_18."AMOUNT_A" AS cash_equivalents,
    line_19."AMOUNT_A" AS outstanding_debts
FROM "CVR_CAMPAIGN_DISCLOSURE_CD" cvr
-- get the numeric filer_id
JOIN "FILER_XREF_CD" x
ON x."XREF_ID" = cvr."FILER_ID"
-- get Monetary Contributions
LEFT JOIN "SMRY_CD" line_1
ON cvr."FILING_ID" = line_1."FILING_ID"
AND cvr."AMEND_ID" = line_1."AMEND_ID"
AND UPPER(line_1."FORM_TYPE") = 'F460'
AND line_1."LINE_ITEM" = '1'
-- get Loans Received
LEFT JOIN "SMRY_CD" line_2
ON cvr."FILING_ID" = line_2."FILING_ID"
AND cvr."AMEND_ID" = line_2."AMEND_ID"
AND UPPER(line_2."FORM_TYPE") = 'F460'
AND line_2."LINE_ITEM" = '2'
-- get Cash Contributions Sub-total
LEFT JOIN "SMRY_CD" line_3
ON cvr."FILING_ID" = line_3."FILING_ID"
AND cvr."AMEND_ID" = line_3."AMEND_ID"
AND UPPER(line_3."FORM_TYPE") = 'F460'
AND line_3."LINE_ITEM" = '3'
-- get Non-monetary Contributions
LEFT JOIN "SMRY_CD" line_4
ON cvr."FILING_ID" = line_4."FILING_ID"
AND cvr."AMEND_ID" = line_4."AMEND_ID"
AND UPPER(line_4."FORM_TYPE") = 'F460'
AND line_4."LINE_ITEM" = '4'
-- get Total Contributions
LEFT JOIN "SMRY_CD" line_5
ON cvr."FILING_ID" = line_5."FILING_ID"
AND cvr."AMEND_ID" = line_5."AMEND_ID"
AND UPPER(line_5."FORM_TYPE") = 'F460'
AND line_5."LINE_ITEM" = '5'
-- get Payments Made
LEFT JOIN "SMRY_CD" line_6
ON cvr."FILING_ID" = line_6."FILING_ID"
AND cvr."AMEND_ID" = line_6."AMEND_ID"
AND UPPER(line_6."FORM_TYPE") = 'F460'
AND line_6."LINE_ITEM" = '6'
-- get Loans Made
LEFT JOIN "SMRY_CD" line_7
ON cvr."FILING_ID" = line_7."FILING_ID"
AND cvr."AMEND_ID" = line_7."AMEND_ID"
AND UPPER(line_7."FORM_TYPE") = 'F460'
AND line_7."LINE_ITEM" = '7'
-- get Cash Payments Sub-total
LEFT JOIN "SMRY_CD" line_8
ON cvr."FILING_ID" = line_8."FILING_ID"
AND cvr."AMEND_ID" = line_8."AMEND_ID"
AND UPPER(line_8."FORM_TYPE") = 'F460'
AND line_8."LINE_ITEM" = '8'
-- get Accrued Expenses (Unpaid Bills)
LEFT JOIN "SMRY_CD" line_9
ON cvr."FILING_ID" = line_9."FILING_ID"
AND cvr."AMEND_ID" = line_9."AMEND_ID"
AND UPPER(line_9."FORM_TYPE") = 'F460'
AND line_9."LINE_ITEM" = '9'
-- get Non-monetary Adjustment
LEFT JOIN "SMRY_CD" line_10
ON cvr."FILING_ID" = line_10."FILING_ID"
AND cvr."AMEND_ID" = line_10."AMEND_ID"
AND UPPER(line_10."FORM_TYPE") = 'F460'
AND line_10."LINE_ITEM" = '10'
-- get Total Expenditures Made
LEFT JOIN "SMRY_CD" line_11
ON cvr."FILING_ID" = line_11."FILING_ID"
AND cvr."AMEND_ID" = line_11."AMEND_ID"
AND UPPER(line_11."FORM_TYPE") = 'F460'
AND line_11."LINE_ITEM" = '11'
-- get Beginning Cash Balance
LEFT JOIN "SMRY_CD" line_12
ON cvr."FILING_ID" = line_12."FILING_ID"
AND cvr."AMEND_ID" = line_12."AMEND_ID"
AND UPPER(line_12."FORM_TYPE") = 'F460'
AND line_12."LINE_ITEM" = '12'
-- get Cash Receipts
LEFT JOIN "SMRY_CD" line_13
ON cvr."FILING_ID" = line_13."FILING_ID"
AND cvr."AMEND_ID" = line_13."AMEND_ID"
AND UPPER(line_13."FORM_TYPE") = 'F460'
AND line_13."LINE_ITEM" = '13'
-- get Miscellaneous Cash Increases
LEFT JOIN "SMRY_CD" line_14
ON cvr."FILING_ID" = line_14."FILING_ID"
AND cvr."AMEND_ID" = line_14."AMEND_ID"
AND UPPER(line_14."FORM_TYPE") = 'F460'
AND line_14."LINE_ITEM" = '14'
-- get Cash Payments
LEFT JOIN "SMRY_CD" line_15
ON cvr."FILING_ID" = line_15."FILING_ID"
AND cvr."AMEND_ID" = line_15."AMEND_ID"
AND UPPER(line_15."FORM_TYPE") = 'F460'
AND line_15."LINE_ITEM" = '15'
-- get Ending Cash Balance
LEFT JOIN "SMRY_CD" line_16
ON cvr."FILING_ID" = line_16."FILING_ID"
AND cvr."AMEND_ID" = line_16."AMEND_ID"
AND UPPER(line_16."FORM_TYPE") = 'F460'
AND line_16."LINE_ITEM" = '16'
-- get Loan Guarantees Received
LEFT JOIN "SMRY_CD" line_17
ON cvr."FILING_ID" = line_17."FILING_ID"
AND cvr."AMEND_ID" = line_17."AMEND_ID"
AND UPPER(line_17."FORM_TYPE") = 'F460'
AND line_17."LINE_ITEM" = '17'
-- get Cash Equivalents
LEFT JOIN "SMRY_CD" line_18
ON cvr."FILING_ID" = line_18."FILING_ID"
AND cvr."AMEND_ID" = line_18."AMEND_ID"
AND UPPER(line_18."FORM_TYPE") = 'F460'
AND line_18."LINE_ITEM" = '18'
-- get Outstanding Debts
LEFT JOIN "SMRY_CD" line_19
ON cvr."FILING_ID" = line_19."FILING_ID"
AND cvr."AMEND_ID" = line_19."AMEND_ID"
AND UPPER(line_19."FORM_TYPE") = 'F460'
AND line_19."LINE_ITEM" = '19'
WHERE cvr."FORM_TYPE" = 'F460';
