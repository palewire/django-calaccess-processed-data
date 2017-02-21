INSERT INTO calaccess_processed_form497filing (
    filing_id,
    amendment_count,
    filer_id,
    date_filed,
    filer_lastname,
    filer_firstname,
    election_date
)
SELECT
    f497.filing_id,
    latest.amendment_count,
    f497.filer_id,
    f497.date_filed,
    f497.filer_lastname,
    f497.filer_firstname,
    f497.election_date
FROM (
    -- get most recent amendment for each filing
    SELECT filing_id, MAX(amend_id) AS amendment_count
    FROM calaccess_processed_form497filingversion
    GROUP BY 1
) AS latest
JOIN calaccess_processed_form497filingversion f497
ON latest.filing_id = f497.filing_id
AND latest.amendment_count = f497.amend_id;
