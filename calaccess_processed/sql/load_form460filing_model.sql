INSERT INTO calaccess_processed_form460filing (
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
    f460.filing_id,
    latest.amendment_count,
    f460.filer_id,
    f460.date_filed,
    f460.from_date,
    f460.thru_date,
    f460.filer_lastname,
    f460.filer_firstname,
    f460.election_date,
    f460.monetary_contributions,
    f460.loans_received,
    f460.subtotal_cash_contributions,
    f460.nonmonetary_contributions,
    f460.total_contributions,
    f460.payments_made,
    f460.loans_made,
    f460.subtotal_cash_payments,
    f460.unpaid_bills,
    f460.nonmonetary_adjustment,
    f460.total_expenditures_made,
    f460.begin_cash_balance,
    f460.cash_receipts,
    f460.miscellaneous_cash_increases,
    f460.cash_payments,
    f460.ending_cash_balance,
    f460.loan_guarantees_received,
    f460.cash_equivalents,
    f460.outstanding_debts
FROM (
    -- get most recent amendment for each filing
    SELECT filing_id, MAX(amend_id) AS amendment_count
    FROM calaccess_processed_form460filingversion
    GROUP BY 1
) AS latest
JOIN calaccess_processed_form460filingversion f460
ON latest.filing_id = f460.filing_id
AND latest.amendment_count = f460.amend_id;