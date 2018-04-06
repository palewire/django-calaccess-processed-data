INSERT INTO calaccess_processed_filings_form501filing (
    filing_id,
    amendment_count,
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
    f501.filing_id,
    latest.amendment_count,
    f501.date_filed,
    f501.statement_type,
    f501.filer_id,
    f501.committee_id,
    f501.title,
    f501.last_name,
    f501.first_name,
    f501.middle_name,
    f501.name_suffix,
    f501.name_moniker,
    f501.phone,
    f501.fax,
    f501.email,
    f501.city,
    f501.state,
    f501.zip_code,
    f501.office,
    f501.agency,
    f501.district,
    f501.party,
    f501.jurisdiction,
    f501.election_type,
    f501.election_year,
    f501.accepted_limit,
    f501.limit_not_exceeded_election_date,
    f501.personal_funds_contrib_date,
    f501.executed_on
FROM (
    -- get most recent amendment for each filing
    SELECT filing_id, MAX(amend_id) AS amendment_count
    FROM calaccess_processed_filings_form501filingversion
    GROUP BY 1
) AS latest
JOIN calaccess_processed_filings_form501filingversion f501
ON latest.filing_id = f501.filing_id
AND latest.amendment_count = f501.amend_id;
