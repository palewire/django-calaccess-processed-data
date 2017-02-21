INSERT INTO calaccess_processed_form497filingversion (
    filing_id,
    amend_id,
    filer_id,
    date_filed,
    filer_lastname,
    filer_firstname,
    election_date
)
SELECT 
    cvr."FILING_ID" AS filing_id,
    cvr."AMEND_ID" AS amend_id,
    x."FILER_ID" AS filer_id,
    cvr."RPT_DATE" AS date_filed,
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
WHERE cvr."FORM_TYPE" = 'F497';