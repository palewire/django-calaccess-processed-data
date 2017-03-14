INSERT INTO calaccess_processed_form460scheduleasummary (
    filing_id,
    itemized_contributions,
    unitemized_contributions,
    total_contributions
)
SELECT
    filing.filing_id AS filing_id,
    line_1."AMOUNT_A" AS itemized_contributions,
    line_2."AMOUNT_A" AS unitemized_contributions,
    line_3."AMOUNT_A" AS total_contributions
FROM calaccess_processed_form460filing filing
-- get itemized contributions
LEFT JOIN "SMRY_CD" line_1
ON filing."filing_id" = line_1."FILING_ID"
AND UPPER(line_1."FORM_TYPE") = 'A'
AND line_1."LINE_ITEM" = '1'
-- get unitemized contributions
LEFT JOIN "SMRY_CD" line_2
ON filing."filing_id" = line_2."FILING_ID"
AND UPPER(line_2."FORM_TYPE") = 'A'
AND line_2."LINE_ITEM" = '2'
-- get total contributions
LEFT JOIN "SMRY_CD" line_3
ON filing."filing_id" = line_3."FILING_ID"
AND UPPER(line_3."FORM_TYPE") = 'A'
AND line_3."LINE_ITEM" = '3';
