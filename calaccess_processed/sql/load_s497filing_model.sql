INSERT INTO calaccess_processed_s497filing (
    filing_id,
    amendment_count,
    filer_id,
    date_filed,
    filer_lastname,
    filer_firstname,
    election_date
)
SELECT
    cvr."FILING_ID" as filing_id,
    last_cvr.last_amend_id as amendment_count,
    x."FILER_ID" as filer_id,
    cvr."RPT_DATE" as date_filed,
    UPPER(cvr."FILER_NAML") as filer_lastname,
    CASE 
        WHEN cvr."FILER_NAMF" IN ('.', '-') THEN ''
        ELSE UPPER(cvr."FILER_NAMF")
    END as filer_firstname,
    cvr."ELECT_DATE" as election_date
FROM (
    -- get most recent amendment for each filing
    SELECT "FILING_ID", MAX("AMEND_ID") AS last_amend_id
    FROM "CVR_CAMPAIGN_DISCLOSURE_CD"
    GROUP BY 1
) AS last_cvr
JOIN "CVR_CAMPAIGN_DISCLOSURE_CD" cvr
ON last_cvr."FILING_ID" = cvr."FILING_ID"
AND last_cvr.last_amend_id = cvr."AMEND_ID"
-- get the numeric filer_id
JOIN "FILER_XREF_CD" x
ON x."XREF_ID" = cvr."FILER_ID"
WHERE cvr."FORM_TYPE" = 'F497';