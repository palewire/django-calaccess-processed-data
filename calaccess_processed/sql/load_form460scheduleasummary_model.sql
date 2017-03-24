INSERT INTO calaccess_processed_form460scheduleasummary (
    filing_id,
    itemized_contributions,
    unitemized_contributions,
    total_contributions
)
SELECT
    filing.filing_id AS filing_id,
    summary_version.itemized_contributions,
    summary_version.unitemized_contributions,
    summary_version.total_contributions
FROM calaccess_processed_form460filing filing
JOIN calaccess_processed_form460filingversion filing_version
ON filing.filing_id = filing_version.filing_id
AND filing.amendment_count = filing_version.amend_id
JOIN calaccess_processed_form460scheduleasummaryversion summary_version
ON filing_version.id = summary_version.filing_version_id;
