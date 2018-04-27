INSERT INTO calaccess_processed_filings_form461filing (
    filing_id,
    amendment_count,
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
    f461.filing_id,
    latest.amendment_count,
    f461.filer_id,
    f461.date_filed,
    f461.statement_type,
    f461.from_date,
    f461.thru_date,
    f461.filer_lastname,
    f461.filer_firstname,
    f461.election_date
FROM (
    -- get most recent amendment for each filing
    SELECT filing_id, MAX(amend_id) AS amendment_count
    FROM calaccess_processed_filings_form461filingversion
    GROUP BY 1
) AS latest
JOIN calaccess_processed_filings_form461filingversion f461
ON latest.filing_id = f461.filing_id
AND latest.amendment_count = f461.amend_id;
