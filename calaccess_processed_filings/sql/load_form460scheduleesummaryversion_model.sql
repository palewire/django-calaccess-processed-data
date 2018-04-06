INSERT INTO calaccess_processed_filings_form460scheduleesummaryversion (
    filing_version_id,
    itemized_expenditures,
    unitemized_expenditures,
    interest_paid,
    total_expenditures
)
SELECT
    filing_version.id AS filing_version_id,
    line_1."AMOUNT_A" AS itemized_expenditures,
    line_2."AMOUNT_A" AS unitemized_expenditures,
    line_3."AMOUNT_A" AS interest_paid,
    line_4."AMOUNT_A" AS total_expenditures
FROM calaccess_processed_filings_form460filingversion filing_version
-- get itemized
LEFT JOIN "SMRY_CD" line_1
ON filing_version."filing_id" = line_1."FILING_ID"
AND filing_version."amend_id" = line_1."AMEND_ID"
AND UPPER(line_1."FORM_TYPE") = 'E'
AND line_1."LINE_ITEM" = '1'
-- get unitemized
LEFT JOIN "SMRY_CD" line_2
ON filing_version."filing_id" = line_2."FILING_ID"
AND filing_version."amend_id" = line_2."AMEND_ID"
AND UPPER(line_2."FORM_TYPE") = 'E'
AND line_2."LINE_ITEM" = '2'
-- get interest
LEFT JOIN "SMRY_CD" line_3
ON filing_version."filing_id" = line_3."FILING_ID"
AND filing_version."amend_id" = line_3."AMEND_ID"
AND UPPER(line_3."FORM_TYPE") = 'E'
AND line_3."LINE_ITEM" = '3'
-- get total
LEFT JOIN "SMRY_CD" line_4
ON filing_version."filing_id" = line_4."FILING_ID"
AND filing_version."amend_id" = line_4."AMEND_ID"
AND UPPER(line_4."FORM_TYPE") = 'E'
AND line_4."LINE_ITEM" = '4';
