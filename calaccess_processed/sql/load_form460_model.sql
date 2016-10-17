INSERT INTO calaccess_processed_form460 (
    filing_id,
    amendment_count,
    filer_id,
    date_filed,
    from_date,
    thru_date,
    filer_lastname,
    filer_firstname,
    election_date,
    monetary_contributions,
    loans_received,
    subtotal_cash_contributions,
    nonmonetary_contributions,
    total_contributions,
    payments_made,
    loans_made,
    subtotal_cash_payments,
    unpaid_bills,
    nonmonetary_adjustment,
    total_expenditures_made,
    begin_cash_balance,
    cash_receipts,
    miscellaneous_cash_increases,
    cash_payments,
    ending_cash_balance,
    loan_guarantees_received,
    cash_equivalents,
    outstanding_debts
)
SELECT 
    f460.filing_id AS filing_id,
    latest.amend_id AS amendment_count,
    f460.filer_id AS filer_id,
    f460.date_filed AS date_filed,
    f460.from_date AS from_date,
    f460.thru_date AS thru_date,
    f460.filer_lastname AS filer_lastname,
    f460.filer_firstname AS filer_firstname,
    f460.election_date AS election_date,
    f460.monetary_contributions AS monetary_contributions,
    f460.loans_received AS loans_received,
    f460.subtotal_cash_contributions AS subtotal_cash_contributions,
    f460.nonmonetary_contributions AS nonmonetary_contributions,
    f460.total_contributions AS total_contributions,
    f460.payments_made AS payments_made,
    f460.loans_made AS loans_made,
    f460.subtotal_cash_payments AS subtotal_cash_payments,
    f460.unpaid_bills AS unpaid_bills,
    f460.nonmonetary_adjustment AS nonmonetary_adjustment,
    f460.total_expenditures_made AS total_expenditures_made,
    f460.begin_cash_balance AS begin_cash_balance,
    f460.cash_receipts AS cash_receipts,
    f460.miscellaneous_cash_increases AS miscellaneous_cash_increases,
    f460.cash_payments AS cash_payments,
    f460.ending_cash_balance AS ending_cash_balance,
    f460.loan_guarantees_received AS loan_guarantees_received,
    f460.cash_equivalents AS cash_equivalents,
    f460.outstanding_debts AS outstanding_debts
FROM (
    -- get most recent amendment for each filing
    SELECT filing_id, MAX(amend_id) AS amend_id
    FROM calaccess_processed_form460version
    GROUP BY 1
) AS latest
JOIN calaccess_processed_form460version f460
ON latest.filing_id = f460.filing_id
AND latest.amend_id = f460.amend_id;