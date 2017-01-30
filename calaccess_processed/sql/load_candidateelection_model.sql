INSERT INTO calaccess_processed_candidateelection (
        filer_id,
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
        COALESCE(x."FILER_ID", ci."FILER_ID"::int) AS filer_id,
        UPPER(ci."CAND_NAMT") AS title,
        UPPER(ci."CAND_NAML") AS last_name,
        UPPER(ci."CAND_NAMF") AS first_name,
        UPPER(ci."CAN_NAMM") AS middle_name,
        UPPER(ci."CAND_NAMS") AS name_suffix,
        dedupe."FILING_ID" AS f501_filing_id,
        dedupe.amend_id AS last_f501_amend_id,
        ci."COMMITTEE_ID" AS controlled_committee_filer_id,
        UPPER(COALESCE(o."CODE_DESC", ci."OFFIC_DSCR")) AS office,
        UPPER(COALESCE(d."CODE_DESC", ci."DIST_NO")) AS district,
        ci."AGENCY_NAM" AS agency,
        UPPER(COALESCE(j."CODE_DESC", '')) AS jurisdiction,
        UPPER(COALESCE(p."CODE_DESC", ci."PARTY")) AS party,
        ci."YR_OF_ELEC" AS election_year,
        ci."CAND_CITY" AS city,
        ci."CAND_ST" AS state,
        ci."CAND_ZIP4" AS zip_code,
        ci."CAND_PHON" AS phone,
        ci."CAND_FAX" AS fax,
        ci."CAND_EMAIL" AS email
  FROM (
        --include only the most recent amendment to each Form 501
        SELECT "FILING_ID", MAX("AMEND_ID") AS amend_id
        FROM "F501_502_CD"
        WHERE "FORM_TYPE" = 'F501'
        GROUP BY 1
    ) AS dedupe
    JOIN "F501_502_CD" AS ci
    ON dedupe."FILING_ID" = ci."FILING_ID"
    AND dedupe.amend_id = ci."AMEND_ID"
    -- get the numeric filer_id
    LEFT JOIN "FILER_XREF_CD" x
    ON ci."FILER_ID" = x."XREF_ID"
    -- include offices
    LEFT JOIN "LOOKUP_CODES_CD" AS o
    ON NULLIF(ci."OFFICE_CD", 0) = o."CODE_ID"
    AND o."CODE_TYPE" IN (30000, 50000)
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
    ON NULLIF(ci."PARTY_CD", 0) = p."CODE_ID"
    AND p."CODE_TYPE" = 16000
-- ignore half a dozen cases where F501_502_CD.FILER_ID is 
WHERE ci."FILER_ID" <> '';
