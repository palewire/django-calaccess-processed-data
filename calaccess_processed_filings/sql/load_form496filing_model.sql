INSERT INTO calaccess_processed_filings_form496filing (
    filing_id,
    amendment_count,
    filer_id,
    date_filed,
    filer_lastname,
    filer_firstname,
    election_date
)
SELECT
    f496.filing_id,
    latest.amendment_count,
    f496.filer_id,
    f496.date_filed,
    f496.filer_lastname,
    f496.filer_firstname,
    f496.election_date
FROM (
    -- get most recent amendment for each filing
    SELECT filing_id, MAX(amend_id) AS amendment_count
    FROM calaccess_processed_filings_form496filingversion
    GROUP BY 1
) AS latest
JOIN calaccess_processed_filings_form496filingversion f496
ON latest.filing_id = f496.filing_id
AND latest.amendment_count = f496.amend_id;
