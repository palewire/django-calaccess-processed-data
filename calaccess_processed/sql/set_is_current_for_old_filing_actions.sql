-- Setting is_current to false for older Filing Actions
UPDATE opencivicdata_filingaction
    SET is_current = false,
    updated_at = now()
FROM opencivicdata_filingaction fa
-- get latest amend_id for each filing
LEFT JOIN (
    SELECT filing_id, MAX((extras->>'amend_id')::int) as amend_id
    FROM opencivicdata_filingaction
    GROUP BY 1
) latest
ON fa.filing_id = latest.filing_id
WHERE latest.amend_id IS NULL
AND fa.is_current = true;
