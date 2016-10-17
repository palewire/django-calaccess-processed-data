INSERT INTO calaccess_processed_latecontributionmade (
    filing_id,
    line_item,
    date_received,
    date_received_thru,
    amount_received,
    transaction_id,
    memo_reference_number,
    recipient_code,
    recipient_committee_id,
    recipient_title,
    recipient_lastname,
    recipient_firstname,
    recipient_name_suffix,
    recipient_city,
    recipient_state,
    recipient_zip,
    candidate_id,
    candidate_title,
    candidate_lastname,
    candidate_firstname,
    candidate_namesuffix,
    candidate_office_code,
    candidate_office_description,
    candidate_jurisdiction_code,
    candidate_jurisdiction_description,
    candidate_district,
    ballot_measure_name,
    ballot_measure_number,
    ballot_measure_jurisdiction,
    support_opposition_code,
    election_date
)
SELECT 
    s497."FILING_ID" AS filing_id,
    s497."LINE_ITEM" AS line_item,
    COALESCE(s497."CTRIB_DATE", s497."DATE_THRU") AS date_received,
    CASE 
        WHEN s497."CTRIB_DATE" IS NULL THEN NULL
        ELSE s497."DATE_THRU" 
    END AS date_received_thru,
    s497."AMOUNT" AS amount_received,
    s497."TRAN_ID" AS transaction_id,
    s497."MEMO_REFNO" AS memo_reference_number,
    CASE s497."ENTITY_CD"
        WHEN '0' THEN ''
        ELSE UPPER(s497."ENTITY_CD")
    END AS recipient_code,
    -- replace '#', '`' and '.' with empty string 
    -- and trim leading/trailing whitespace
    TRIM(
        REPLACE(REPLACE(REPLACE(s497."CMTE_ID", '#', ''), '`', ''), '.', '')
    ) AS recipient_committee_id,
    UPPER(s497."ENTY_NAMT") AS recipient_title,
    UPPER(s497."ENTY_NAML") AS recipient_lastname,
    UPPER(s497."ENTY_NAMF") AS recipient_firstname,
    UPPER(s497."ENTY_NAMS") AS recipient_name_suffix,
    UPPER(s497."ENTY_CITY") AS recipient_city,
    UPPER(s497."ENTY_ST") AS recipient_state,
    UPPER(s497."ENTY_ZIP4") AS recipient_zip,
    UPPER(s497."CAND_ID") AS candidate_id,
    UPPER(s497."CAND_NAMT") AS candidate_title,
    UPPER(s497."CAND_NAML") AS candidate_lastname,
    UPPER(s497."CAND_NAMF") AS candidate_firstname,
    UPPER(s497."CAND_NAMS") AS candidate_namesuffix,
    UPPER(s497."OFFICE_CD") AS candidate_office_code,
    UPPER(s497."OFFIC_DSCR") AS candidate_office_description,
    UPPER(s497."JURIS_CD") AS candidate_jurisdiction_code,
    UPPER(s497."JURIS_DSCR") AS candidate_jurisdiction_description,
    UPPER(s497."DIST_NO") AS candidate_district,
    UPPER(s497."BAL_NAME") AS ballot_measure_name,
    UPPER(s497."BAL_NUM") AS ballot_measure_number,
    UPPER(s497."BAL_JURIS") AS ballot_measure_jurisdiction,
    UPPER(s497."SUP_OPP_CD") AS support_opposition_code,
    s497."ELEC_DATE" AS election_date
FROM (
    SELECT "FILING_ID", MAX("AMEND_ID") AS amend_id
    FROM "S497_CD"
    GROUP BY 1
) latest
JOIN "S497_CD" s497
ON latest."FILING_ID" = s497."FILING_ID"
AND latest.amend_id = s497."AMEND_ID"
WHERE s497."FORM_TYPE" = 'F497P2';