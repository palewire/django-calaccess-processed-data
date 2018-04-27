INSERT INTO calaccess_processed_filings_form461filingversion (
    filing_id,
    amend_id,
    filer_id,
    date_filed,
    statement_type,
    from_date,
    thru_date,
    filer_lastname,
    filer_firstname,
    election_date
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
    cvr."ELECT_DATE" AS election_date
FROM "CVR_CAMPAIGN_DISCLOSURE_CD" cvr
-- get the numeric filer_id
JOIN "FILER_XREF_CD" x
ON x."XREF_ID" = cvr."FILER_ID"
WHERE cvr."FORM_TYPE" = 'F461';
