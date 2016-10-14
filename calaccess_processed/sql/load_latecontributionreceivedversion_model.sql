INSERT INTO calaccess_processed_latecontributionreceivedversion (
    filing_id,
    amend_id,
    line_item,
    date_received,
    date_received_thru,
    amount_received,
    transaction_id,
    memo_reference_number,
    contributor_code,
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
    committee_id
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
    END AS contributor_code,
    UPPER("ENTY_NAMT") AS contributor_title,
    UPPER("ENTY_NAML") AS contributor_lastname,
    UPPER("ENTY_NAMF") AS contributor_firstname,
    UPPER("ENTY_NAMS") AS contributor_name_suffix,
    UPPER("ENTY_CITY") AS contributor_city,
    UPPER("ENTY_ST") AS contributor_state,
    UPPER("ENTY_ZIP4") AS contributor_zip,
    UPPER("CTRIB_EMP") AS contributor_employer,
    UPPER("CTRIB_OCC") AS contributor_occupation,
    CASE "CTRIB_SELF"
        WHEN 'y' THEN true
        WHEN 'X' THEN true
        WHEN 'n' THEN false
        WHEN '0' THEN false
        ELSE false 
    END AS contributor_is_self_employed,
    -- replace '#', '`' and '.' with empty string 
    -- and trim leading/trailing whitespace
    TRIM(
        REPLACE(REPLACE(REPLACE("CMTE_ID", '#', ''), '`', ''), '.', '')
    ) AS committee_id
FROM "S497_CD"
WHERE "FORM_TYPE" = 'F497P1';