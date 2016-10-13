INSERT INTO calaccess_processed_s497filingversion (
    filing_id,
    amend_id,
    filer_id,
    date_filed,
    filer_lastname,
    filer_firstname,
    election_date
)
SELECT 
    cvr."FILING_ID" as filing_id,
    cvr."AMEND_ID" as amend_id,
    x."FILER_ID" as filer_id,
    cvr."RPT_DATE" as date_filed,
    UPPER(cvr."FILER_NAML") as filer_lastname,
    CASE 
        WHEN cvr."FILER_NAMF" IN ('.', '-') THEN ''
        ELSE UPPER(cvr."FILER_NAMF")
    END as filer_firstname,
    cvr."ELECT_DATE" as election_date
FROM "CVR_CAMPAIGN_DISCLOSURE_CD" cvr
-- get the numeric filer_id
JOIN "FILER_XREF_CD" x
ON x."XREF_ID" = cvr."FILER_ID"
WHERE cvr."FORM_TYPE" = 'F497';