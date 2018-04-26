INSERT INTO calaccess_processed_filings_form496part1itemversion (
    filing_version_id,
    candidate_title,
    candidate_lastname,
    candidate_firstname,
    candidate_name_suffix,
    candidate_id,
    candidate_office_code,
    ballot_measure_name,
    ballot_measure_number,
    ballot_measure_jurisdiction,
    support_opposition_code
)
SELECT
    filing_version.id AS filing_version_id,
    UPPER(cvr."CAND_NAMT") AS candidate_title,
    UPPER(cvr."CAND_NAML") AS candidate_lastname,
    UPPER(cvr."CAND_NAMF") AS candidate_firstname,
    UPPER(cvr."CAND_NAMS") AS candidate_namesuffix,
    -- replace '#', '`' and '.' with empty string
    -- and trim leading/trailing whitespace
    TRIM(
        REPLACE(REPLACE(REPLACE(cvr."CAND_ID", '#', ''), '`', ''), '.', '')
    ) AS candidate_id,
    UPPER(cvr."OFFICE_CD") AS candidate_office_code,
    UPPER(cvr."BAL_NAME") AS ballot_measure_name,
    UPPER(cvr."BAL_NUM") AS ballot_measure_number,
    UPPER(cvr."BAL_JURIS") AS ballot_measure_jurisdiction,
    UPPER(cvr."SUP_OPP_CD") AS support_opposition_code
FROM "CVR_CAMPAIGN_DISCLOSURE_CD" cvr
JOIN calaccess_processed_filings_form496filingversion filing_version
ON cvr."FILING_ID" = filing_version.filing_id
AND cvr."AMEND_ID" = filing_version.amend_id
WHERE cvr."FORM_TYPE" = 'F496';
