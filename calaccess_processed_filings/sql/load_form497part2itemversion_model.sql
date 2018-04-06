INSERT INTO calaccess_processed_filings_form497part2itemversion (
    filing_version_id,
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
    filing_version.id AS filing_version_id,
    s497_line."LINE_ITEM" AS line_item,
    COALESCE(s497_line."CTRIB_DATE", s497_line."DATE_THRU") AS date_received,
    CASE
        WHEN s497_line."CTRIB_DATE" IS NULL THEN NULL
        ELSE s497_line."DATE_THRU"
    END AS date_received_thru,
    s497_line."AMOUNT" AS amount_received,
    s497_line."TRAN_ID" AS transaction_id,
    s497_line."MEMO_REFNO" AS memo_reference_number,
    CASE s497_line."ENTITY_CD"
        WHEN '0' THEN ''
        ELSE UPPER(s497_line."ENTITY_CD")
    END AS recipient_code,
    -- replace '#', '`' and '.' with empty string
    -- and trim leading/trailing whitespace
    TRIM(
        REPLACE(REPLACE(REPLACE(s497_line."CMTE_ID", '#', ''), '`', ''), '.', '')
    ) AS recipient_committee_id,
    UPPER(s497_line."ENTY_NAMT") AS recipient_title,
    UPPER(s497_line."ENTY_NAML") AS recipient_lastname,
    UPPER(s497_line."ENTY_NAMF") AS recipient_firstname,
    UPPER(s497_line."ENTY_NAMS") AS recipient_name_suffix,
    UPPER(s497_line."ENTY_CITY") AS recipient_city,
    UPPER(s497_line."ENTY_ST") AS recipient_state,
    UPPER(s497_line."ENTY_ZIP4") AS recipient_zip,
    UPPER(s497_line."CAND_ID") AS candidate_id,
    UPPER(s497_line."CAND_NAMT") AS candidate_title,
    UPPER(s497_line."CAND_NAML") AS candidate_lastname,
    UPPER(s497_line."CAND_NAMF") AS candidate_firstname,
    UPPER(s497_line."CAND_NAMS") AS candidate_namesuffix,
    UPPER(s497_line."OFFICE_CD") AS candidate_office_code,
    UPPER(s497_line."OFFIC_DSCR") AS candidate_office_description,
    UPPER(s497_line."JURIS_CD") AS candidate_jurisdiction_code,
    UPPER(s497_line."JURIS_DSCR") AS candidate_jurisdiction_description,
    UPPER(s497_line."DIST_NO") AS candidate_district,
    UPPER(s497_line."BAL_NAME") AS ballot_measure_name,
    UPPER(s497_line."BAL_NUM") AS ballot_measure_number,
    UPPER(s497_line."BAL_JURIS") AS ballot_measure_jurisdiction,
    UPPER(s497_line."SUP_OPP_CD") AS support_opposition_code,
    s497_line."ELEC_DATE" AS election_date
FROM "S497_CD" s497_line
JOIN calaccess_processed_filings_form497filingversion filing_version
ON s497_line."FILING_ID" = filing_version.filing_id
AND s497_line."AMEND_ID" = filing_version.amend_id
WHERE s497_line."FORM_TYPE" = 'F497P2';
