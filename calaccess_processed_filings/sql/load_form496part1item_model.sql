INSERT INTO calaccess_processed_filings_form496part1item (
    filing_id,
    candidate_title,
    candidate_lastname,
    candidate_firstname,
    candidate_name_suffix,
    candidate_id,
    candidate_office_code,
    ballot_measure_name,
    ballot_measure_number,
    ballot_measure_jurisdiction,
    support_opposition_code
)
SELECT
    filing.filing_id,
    item_version.candidate_title,
    item_version.candidate_lastname,
    item_version.candidate_firstname,
    item_version.candidate_name_suffix,
    item_version.candidate_id,
    item_version.candidate_office_code,
    item_version.ballot_measure_name,
    item_version.ballot_measure_number,
    item_version.ballot_measure_jurisdiction,
    item_version.support_opposition_code
FROM calaccess_processed_filings_form496filing filing
JOIN calaccess_processed_filings_form496filingversion filing_version
ON filing.filing_id = filing_version.filing_id
AND filing.amendment_count = filing_version.amend_id
JOIN calaccess_processed_filings_form496part1itemversion item_version
ON filing_version.id = item_version.filing_version_id;
