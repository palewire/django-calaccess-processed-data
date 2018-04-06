INSERT INTO calaccess_processed_filings_form460schedulefitemversion (
    filing_version_id,
    line_item,
    payee_code,
    payee_committee_id,
    payee_title,
    payee_lastname,
    payee_firstname,
    payee_name_suffix,
    payee_city,
    payee_state,
    payee_zip,
    treasurer_title,
    treasurer_lastname,
    treasurer_firstname,
    treasurer_name_suffix,
    treasurer_city,
    treasurer_state,
    payment_code,
    payment_description,
    begin_balance,
    amount_paid,
    amount_incurred,
    end_balance,
    transaction_id,
    parent_transaction_id,
    memo_reference_number,
    memo_code
)
SELECT
    filing_version.id AS filing_version_id,
    debt."LINE_ITEM" AS line_item,
    CASE
        WHEN UPPER(debt."ENTITY_CD") IN (
            'BNM',
            'COM',
            'IND',
            'OTH',
            'PTY',
            'RCP',
            'SCC',
            ''
        ) THEN UPPER(debt."ENTITY_CD")
        ELSE '???'
    END AS payee_code,
    -- remove substrings like 'ID', 'I.D.', 'IC:', then remove '#'
    -- then trim leading/trailing whitespace
    -- btw...still a lot of cruft in this column
    TRIM(
        REPLACE(
            REGEXP_REPLACE(
                UPPER("CMTE_ID"),
                'I\.?[CD]\.?:?',
                ''
            ),
            '#',
            ''
        )
    ) AS payee_committee_id,
    UPPER(debt."PAYEE_NAMT") AS payee_title,
    UPPER(debt."PAYEE_NAML") AS payee_lastname,
    UPPER(debt."PAYEE_NAMF") AS payee_firstname,
    UPPER(debt."PAYEE_NAMS") AS payee_name_suffix,
    UPPER(debt."PAYEE_CITY") AS payee_city,
    UPPER(debt."PAYEE_ST") AS payee_state,
    UPPER(debt."PAYEE_ZIP4") AS payee_zip,
    UPPER(debt."TRES_NAMT") AS treasurer_title,
    UPPER(debt."TRES_NAML") AS treasurer_lastname,
    UPPER(debt."TRES_NAMF") AS treasurer_firstname,
    UPPER(debt."TRES_NAMS") AS treasurer_name_suffix,
    UPPER(debt."TRES_CITY") AS treasurer_city,
    UPPER(debt."TRES_ST") AS treasurer_state,
    CASE
        WHEN UPPER(debt."EXPN_CODE") IN (
            'CMP',
            'CNS',
            'CTB',
            'CVC',
            'FIL',
            'FND',
            'IKD',
            'IND',
            'LEG',
            'LIT',
            'LON',
            'MBR',
            'MON',
            'MTG',
            'OFC',
            'PET',
            'PHO',
            'POL',
            'POS',
            'PRO',
            'PRT',
            'RAD',
            'RFD',
            'SAL',
            'TEL',
            'TRC',
            'TRS',
            'TSF',
            'VOT',
            'WEB',
            ''
        ) THEN UPPER(debt."EXPN_CODE")
        ELSE '???'
    END AS payment_code,
    debt."EXPN_DSCR" AS payment_description,
    debt."BEG_BAL" AS begin_balance,
    debt."AMT_PAID" AS amount_paid,
    debt."AMT_INCUR" AS amount_incurred,
    debt."END_BAL" AS end_balance,
    debt."TRAN_ID" AS transaction_id,
    debt."BAKREF_TID" AS parent_transaction_id,
    debt."MEMO_REFNO" AS memo_reference_number,
    CASE
        WHEN UPPER(debt."MEMO_CODE") IN ('Y', 'X') THEN true
        ELSE false
    END AS memo_code
FROM "DEBT_CD" debt
JOIN calaccess_processed_filings_form460filingversion filing_version
ON debt."FILING_ID" = filing_version.filing_id
AND debt."AMEND_ID" = filing_version.amend_id;
