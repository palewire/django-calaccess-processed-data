INSERT INTO calaccess_processed_form460schedulecsummaryversion (
    filing_version_id,
    itemized_contributions,
    unitemized_contributions,
    total_contributions
)
SELECT
    filing_version.id AS filing_version_id,
    line_1."AMOUNT_A" AS itemized_contributions,
    line_2."AMOUNT_A" AS unitemized_contributions,
    line_3."AMOUNT_A" AS total_contributions
FROM calaccess_processed_form460filingversion filing_version
-- get itemized contributions
LEFT JOIN "SMRY_CD" line_1
ON filing_version."filing_id" = line_1."FILING_ID"
AND filing_version."amend_id" = line_1."AMEND_ID"
AND UPPER(line_1."FORM_TYPE") = 'C'
AND line_1."LINE_ITEM" = '1'
-- get unitemized contributions
LEFT JOIN "SMRY_CD" line_2
ON filing_version."filing_id" = line_2."FILING_ID"
AND filing_version."amend_id" = line_2."AMEND_ID"
AND UPPER(line_2."FORM_TYPE") = 'C'
AND line_2."LINE_ITEM" = '2'
-- get total contributions
LEFT JOIN "SMRY_CD" line_3
ON filing_version."filing_id" = line_3."FILING_ID"
AND filing_version."amend_id" = line_3."AMEND_ID"
AND UPPER(line_3."FORM_TYPE") = 'C'
AND line_3."LINE_ITEM" = '3';
