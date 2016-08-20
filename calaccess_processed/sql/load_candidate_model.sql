INSERT INTO calaccess_processed_candidate (
    filer_id,
    full_name,
    office,
    district,
    agency,
    party,
    election_year,
    city,
    state,
    zip_code,
    phone,
    fax,
    email
)
SELECT
    ff."FILER_ID",
    REPLACE(
        TRIM(
            CONCAT(ci."CAND_NAMT", ' ', ci."CAND_NAMF", ' ', ci."CAND_NAML", ' ', ci."CAND_NAMS")
        ),
        '  ',
        ' '
    ) as full_name,
    o."CODE_DESC" as office,
    d."CODE_DESC" as district,
    ci."AGENCY_NAM" as agency,
    p."CODE_DESC" as party,
    ci."YR_OF_ELEC" as election_year,
    ci."CAND_CITY" as city,
    ci."CAND_ST" as st,
    ci."CAND_ZIP4" as zip,
    ci."CAND_PHON" as phone,
    ci."CAND_FAX" as fax,
    ci."CAND_EMAIL" as email
FROM (
        --include only the most recent amendment to each filers Form 501 (Candidate Intention)
        SELECT "FILER_ID", "FILING_ID", MAX("FILING_SEQUENCE") as amend_id
        FROM "FILER_FILINGS_CD" 
        WHERE "FORM_ID" = 'F501'
        GROUP BY 1, 2
) as ff
JOIN "F501_502_CD" as ci
ON ff."FILING_ID" = ci."FILING_ID"
AND ff.amend_id = ci."AMEND_ID"
-- include office
JOIN "LOOKUP_CODES_CD" as o
ON ci."OFFICE_CD" = o."CODE_ID"
AND o."CODE_TYPE" IN (30000, 50000)
AND ci."OFFICE_CD" <> 0
-- include district
LEFT JOIN "LOOKUP_CODES_CD" as d
ON ci."DISTRICT_CD" = d."CODE_ID"
AND d."CODE_TYPE" = 17000
-- include party
LEFT JOIN "LOOKUP_CODES_CD" as p
ON ci."PARTY_CD" = p."CODE_ID"
AND p."CODE_TYPE" = 16000;
