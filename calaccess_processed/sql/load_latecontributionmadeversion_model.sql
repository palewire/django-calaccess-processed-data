INSERT INTO calaccess_processed_latecontributionmadeversion (
    filing_id,
    amend_id,
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
    "FILING_ID" AS filing_id,
    "AMEND_ID" AS amend_id,
    "LINE_ITEM" AS line_item,
    COALESCE("CTRIB_DATE", "DATE_THRU") AS date_received,
    CASE 
        WHEN "CTRIB_DATE" IS NULL THEN NULL
        ELSE "DATE_THRU" 
    END AS date_received_thru,
    "AMOUNT" AS amount_received,
    "TRAN_ID" AS transaction_id,
    "MEMO_REFNO" AS memo_reference_number,
    CASE "ENTITY_CD"
        WHEN '0' THEN ''
        ELSE UPPER("ENTITY_CD")
    END AS recipient_code,
    -- replace '#', '`' and '.' with empty string 
    -- and trim leading/trailing whitespace
    TRIM(
        REPLACE(REPLACE(REPLACE("CMTE_ID", '#', ''), '`', ''), '.', '')
    ) AS recipient_committee_id,
    UPPER("ENTY_NAMT") AS recipient_title,
    UPPER("ENTY_NAML") AS recipient_lastname,
    UPPER("ENTY_NAMF") AS recipient_firstname,
    UPPER("ENTY_NAMS") AS recipient_name_suffix,
    UPPER("ENTY_CITY") AS recipient_city,
    UPPER("ENTY_ST") AS recipient_state,
    UPPER("ENTY_ZIP4") AS recipient_zip,
    UPPER("CAND_ID") AS candidate_id,
    UPPER("CAND_NAMT") AS candidate_title,
    UPPER("CAND_NAML") AS candidate_lastname,
    UPPER("CAND_NAMF") AS candidate_firstname,
    UPPER("CAND_NAMS") AS candidate_namesuffix,
    UPPER("OFFICE_CD") AS candidate_office_code,
    UPPER("OFFIC_DSCR") AS candidate_office_description,
    UPPER("JURIS_CD") AS candidate_jurisdiction_code,
    UPPER("JURIS_DSCR") AS candidate_jurisdiction_description,
    UPPER("DIST_NO") AS candidate_district,
    UPPER("BAL_NAME") AS ballot_measure_name,
    UPPER("BAL_NUM") AS ballot_measure_number,
    UPPER("BAL_JURIS") AS ballot_measure_jurisdiction,
    UPPER("SUP_OPP_CD") AS support_opposition_code,
    "ELEC_DATE" AS election_date
FROM "S497_CD"
WHERE "FORM_TYPE" = 'F497P2';