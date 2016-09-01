INSERT INTO calaccess_processed_candidate (
    f501_filer_id,
    title,
    last_name,
    first_name,
    middle_name,
    name_suffix,
    f501_filing_id,
    last_f501_amend_id,
    controlled_committee_filer_id,
    office,
    district,
    agency,
    jurisdiction,
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
    ci."FILER_ID" as f501_filer_id,
    ci."CAND_NAMT" as title,
    ci."CAND_NAML" as last_name,
    ci."CAND_NAMF" as first_name,
    ci."CAN_NAMM" as middle_name,
    ci."CAND_NAMS" as name_suffix,
    dedupe."FILING_ID" as f501_filing_id,
    dedupe.amend_id as last_f501_amend_id,
    ci."COMMITTEE_ID" as controlled_committee_filer_id,
    UPPER(COALESCE(o."CODE_DESC", ci."OFFIC_DSCR")) as office,
    UPPER(COALESCE(d."CODE_DESC", ci."DIST_NO")) as district,
    ci."AGENCY_NAM" as agency,
    UPPER(COALESCE(j."CODE_DESC", '')) as jurisdiction,
    UPPER(COALESCE(p."CODE_DESC", ci."PARTY")) as party,
    ci."YR_OF_ELEC" as election_year,
    ci."CAND_CITY" as city,
    ci."CAND_ST" as state,
    ci."CAND_ZIP4" as zip_code,
    ci."CAND_PHON" as phone,
    ci."CAND_FAX" as fax,
    ci."CAND_EMAIL" as email
FROM (
    --include only the most recent amendment to each Form 501
    SELECT "FILING_ID", MAX("AMEND_ID") as amend_id
    FROM "F501_502_CD"
    WHERE "FORM_TYPE" = 'F501'
    GROUP BY 1
) as dedupe
JOIN "F501_502_CD" as ci
ON dedupe."FILING_ID" = ci."FILING_ID"
AND dedupe.amend_id = ci."AMEND_ID"
-- include offices
LEFT JOIN "LOOKUP_CODES_CD" as o
ON NULLIF(ci."OFFICE_CD", 0) = o."CODE_ID"
AND o."CODE_TYPE" IN (30000, 50000)
-- include districts
LEFT JOIN "LOOKUP_CODES_CD" as d
ON NULLIF(ci."DISTRICT_CD", 0) = d."CODE_ID"
AND d."CODE_TYPE" = 17000
-- include jurisdictions
LEFT JOIN "LOOKUP_CODES_CD" as j
ON NULLIF(ci."JURIS_CD", 0) = j."CODE_ID"
AND j."CODE_TYPE" = 40500
-- include party
LEFT JOIN "LOOKUP_CODES_CD" as p
ON NULLIF(ci."PARTY_CD", 0) = p."CODE_ID"
AND p."CODE_TYPE" = 16000;
