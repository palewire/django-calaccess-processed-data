INSERT INTO calaccess_processed_filings_form501filingversion (
    filing_id,
    amend_id,
    date_filed,
    statement_type,
    filer_id,
    committee_id,
    title,
    last_name,
    first_name,
    middle_name,
    name_suffix,
    name_moniker,
    phone,
    fax,
    email,
    city,
    state,
    zip_code,
    office,
    agency,
    district,
    party,
    jurisdiction,
    election_type,
    election_year,
    accepted_limit,
    limit_not_exceeded_election_date,
    personal_funds_contrib_date,
    executed_on
)
SELECT
    ci."FILING_ID" AS filing_id,
    ci."AMEND_ID" AS amend_id,
    ci."RPT_DATE" AS date_filed,
    ci."STMT_TYPE" AS statement_type,
    ci."FILER_ID" AS filer_id,
    ci."COMMITTEE_ID" AS committee_id,
    UPPER(ci."CAND_NAMT") AS title,
    UPPER(ci."CAND_NAML") AS last_name,
    UPPER(ci."CAND_NAMF") AS first_name,
    UPPER(ci."CAN_NAMM") AS middle_name,
    UPPER(ci."CAND_NAMS") AS name_suffix,
    UPPER(ci."MONIKER") AS name_moniker,
    ci."CAND_PHON" as phone,
    ci."CAND_FAX" as fax,
    ci."CAND_EMAIL" as email,
    ci."CAND_CITY" AS city,
    ci."CAND_ST" AS state,
    ci."CAND_ZIP4" AS zip_code,
    INITCAP(COALESCE(o."CODE_DESC", ci."OFFIC_DSCR")) AS office,
    ci."AGENCY_NAM" AS agency,
    COALESCE(d."CODE_DESC", NULLIF(ci."DIST_NO", ''))::int AS district,
    CASE UPPER(COALESCE(p."CODE_DESC", ci."PARTY"))
        WHEN 'AI' THEN 'AMERICAN INDEPENDENT PARTY'
        WHEN 'D' THEN 'DEMOCRATIC'
        WHEN 'DEMOCRAT' THEN 'DEMOCRATIC'
        WHEN 'G' THEN 'GREEN PARTY'
        WHEN 'I' THEN 'INDEPENDENT'
        WHEN 'L' THEN 'LIBERTARIAN'
        WHEN 'NP' THEN 'NON PARTISAN'
        WHEN 'R' THEN 'REPUBLICAN'
        ELSE UPPER(COALESCE(p."CODE_DESC", ci."PARTY"))
    END AS party,
    INITCAP(COALESCE(j."CODE_DESC", '')) AS jurisdiction,
    UPPER(e."CODE_DESC") AS election_type,
    ci."YR_OF_ELEC" AS election_year,
    ci."ACCEPT_LIMIT_YN"::boolean AS accepted_limit,
    ci."DID_EXCEED_DT" AS limit_not_exceeded_election_date,
    ci."CNTRB_PRSNL_FNDS_DT" AS personal_funds_contrib_date,
    ci."EXECUTE_DT" AS executed_on
FROM "F501_502_CD" AS ci
-- include offices
LEFT JOIN "LOOKUP_CODES_CD" AS o
ON NULLIF(ci."OFFICE_CD", 0) = o."CODE_ID"
AND o."CODE_TYPE" = 30000
-- include districts
LEFT JOIN "LOOKUP_CODES_CD" AS d
ON NULLIF(ci."DISTRICT_CD", 0) = d."CODE_ID"
AND d."CODE_TYPE" = 17000
-- include jurisdictions
LEFT JOIN "LOOKUP_CODES_CD" AS j
ON NULLIF(ci."JURIS_CD", 0) = j."CODE_ID"
AND j."CODE_TYPE" = 40500
-- include party
LEFT JOIN "LOOKUP_CODES_CD" AS p
ON ci."PARTY_CD" = p."CODE_ID"
AND p."CODE_TYPE" = 16000
-- election type
LEFT JOIN "LOOKUP_CODES_CD" AS e
ON NULLIF(ci."ELEC_TYPE", 0) = e."CODE_ID"
and e."CODE_TYPE" = 3000
WHERE ci."FORM_TYPE" = 'F501';
