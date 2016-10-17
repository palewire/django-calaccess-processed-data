INSERT INTO calaccess_processed_schedule497 (
    filing_id,
    amendment_count,
    filer_id,
    date_filed,
    filer_lastname,
    filer_firstname,
    election_date
)
SELECT
    s497.filing_id AS filing_id,
    latest.amend_id AS amendment_count,
    s497.filer_id AS filer_id,
    s497.date_filed AS date_filed,
    s497.filer_lastname AS filer_lastname,
    s497.filer_firstname AS filer_firstname,
    s497.election_date AS election_date
FROM (
    -- get most recent amendment for each filing
    SELECT filing_id, MAX(amend_id) AS amend_id
    FROM calaccess_processed_schedule497version
    GROUP BY 1
) AS latest
JOIN calaccess_processed_schedule497version s497
ON latest.filing_id = s497.filing_id
AND latest.amend_id = s497.amend_id;
