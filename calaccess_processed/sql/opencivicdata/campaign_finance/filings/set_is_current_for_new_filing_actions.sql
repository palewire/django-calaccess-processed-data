-- Setting is_current to true for latest Filing Actions
UPDATE opencivicdata_filingaction
    SET is_current = true,
    updated_at = now()
FROM opencivicdata_filingaction fa
-- get latest amend_id for each filing
JOIN (
    SELECT filing_id, MAX((extras->>'amend_id')::int) as amend_id
    FROM opencivicdata_filingaction
    GROUP BY 1
) latest
ON fa.filing_id = latest.filing_id
AND (fa.extras->>'amend_id')::int = latest.amend_id
AND fa.is_current = false;
