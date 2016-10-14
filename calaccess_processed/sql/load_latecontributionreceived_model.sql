INSERT INTO calaccess_processed_latecontributionreceived (
    filing_id,
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
    END AS contributor_code,
    UPPER(s497."ENTY_NAMT") AS contributor_title,
    UPPER(s497."ENTY_NAML") AS contributor_lastname,
    UPPER(s497."ENTY_NAMF") AS contributor_firstname,
    UPPER(s497."ENTY_NAMS") AS contributor_name_suffix,
    UPPER(s497."ENTY_CITY") AS contributor_city,
    UPPER(s497."ENTY_ST") AS contributor_state,
    UPPER(s497."ENTY_ZIP4") AS contributor_zip,
    UPPER(s497."CTRIB_EMP") AS contributor_employer,
    UPPER(s497."CTRIB_OCC") AS contributor_occupation,
    CASE s497."CTRIB_SELF"
        WHEN 'y' THEN true
        WHEN 'X' THEN true
        WHEN 'n' THEN false
        WHEN '0' THEN false
        ELSE false 
    END AS contributor_is_self_employed,
    -- replace '#', '`' and '.' with empty string 
    -- and trim leading/trailing whitespace
    TRIM(
        REPLACE(REPLACE(REPLACE(s497."CMTE_ID", '#', ''), '`', ''), '.', '')
    ) AS committee_id
FROM (
    SELECT "FILING_ID", MAX("AMEND_ID") AS amend_id
    FROM "S497_CD"
    GROUP BY 1
) latest
JOIN "S497_CD" s497
ON latest."FILING_ID" = S497."FILING_ID"
AND latest.amend_id = S497."AMEND_ID"
WHERE s497."FORM_TYPE" = 'F497P1';