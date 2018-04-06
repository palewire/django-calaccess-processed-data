INSERT INTO calaccess_processed_filings_form497part1itemversion (
    filing_version_id,
    line_item,
    date_received,
    date_received_thru,
    amount_received,
    transaction_id,
    memo_reference_number,
    contributor_code,
    contributor_committee_id,
    contributor_title,
    contributor_lastname,
    contributor_firstname,
    contributor_name_suffix,
    contributor_city,
    contributor_state,
    contributor_zip,
    contributor_employer,
    contributor_occupation,
    contributor_is_self_employed
)
SELECT
    filing_version.id AS filing_version_id,
    "LINE_ITEM" AS line_item,
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
    END AS contributor_code,
    -- replace '#', '`' and '.' with empty string
    -- and trim leading/trailing whitespace
    TRIM(
        REPLACE(REPLACE(REPLACE(s497_line."CMTE_ID", '#', ''), '`', ''), '.', '')
    ) AS contributor_committee_id,
    UPPER(s497_line."ENTY_NAMT") AS contributor_title,
    UPPER(s497_line."ENTY_NAML") AS contributor_lastname,
    UPPER(s497_line."ENTY_NAMF") AS contributor_firstname,
    UPPER(s497_line."ENTY_NAMS") AS contributor_name_suffix,
    UPPER(s497_line."ENTY_CITY") AS contributor_city,
    UPPER(s497_line."ENTY_ST") AS contributor_state,
    UPPER(s497_line."ENTY_ZIP4") AS contributor_zip,
    UPPER(s497_line."CTRIB_EMP") AS contributor_employer,
    UPPER(s497_line."CTRIB_OCC") AS contributor_occupation,
    CASE UPPER(s497_line."CTRIB_SELF")
        WHEN 'Y' THEN true
        WHEN 'X' THEN true
        ELSE false
    END AS contributor_is_self_employed
FROM "S497_CD" s497_line
JOIN calaccess_processed_filings_form497filingversion filing_version
ON s497_line."FILING_ID" = filing_version.filing_id
AND s497_line."AMEND_ID" = filing_version.amend_id
WHERE s497_line."FORM_TYPE" = 'F497P1';
