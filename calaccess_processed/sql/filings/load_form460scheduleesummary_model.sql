INSERT INTO calaccess_processed_form460scheduleesummary (
    filing_id,
    itemized_expenditures,
    unitemized_expenditures,
    interest_paid,
    total_expenditures
)
SELECT
    filing.filing_id AS filing_id,
    summary_version.itemized_expenditures,
    summary_version.unitemized_expenditures,
    summary_version.interest_paid,
    summary_version.total_expenditures
FROM calaccess_processed_form460filing filing
JOIN calaccess_processed_form460filingversion filing_version
ON filing.filing_id = filing_version.filing_id
AND filing.amendment_count = filing_version.amend_id
JOIN calaccess_processed_form460scheduleesummaryversion summary_version
ON filing_version.id = summary_version.filing_version_id;
