INSERT INTO calaccess_processed_scheduleesubitemversion (
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
    treasurer_zip,
    payment_code,
    payment_description,
    amount,
    payment_date,
    check_number,
    transaction_id,
    parent_transaction_id,
    memo_reference_number
)
SELECT 
    filing_version.id AS filing_version_id,
    expn."LINE_ITEM" AS line_item,
    CASE
        WHEN UPPER(expn."ENTITY_CD") IN (
            'BNM',
            'CAO',
            'COM',
            'IND',
            'MBR',
            'OFF',
            'OTH',
            'PTY',
            'RCP',
            'SCC'
        ) THEN UPPER(expn."ENTITY_CD")
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
    UPPER(expn."PAYEE_NAMT") AS payee_title,
    UPPER(expn."PAYEE_NAML") AS payee_lastname,
    UPPER(expn."PAYEE_NAMF") AS payee_firstname,
    UPPER(expn."PAYEE_NAMS") AS payee_name_suffix,
    UPPER(expn."PAYEE_CITY") AS payee_city,
    UPPER(expn."PAYEE_ST") AS payee_state,
    UPPER(expn."PAYEE_ZIP4") AS payee_zip,
    UPPER(expn."TRES_NAMT") AS treasurer_title,
    UPPER(expn."TRES_NAML") AS treasurer_lastname,
    UPPER(expn."TRES_NAMF") AS treasurer_firstname,
    UPPER(expn."TRES_NAMS") AS treasurer_name_suffix,
    UPPER(expn."TRES_CITY") AS treasurer_city,
    UPPER(expn."TRES_ST") AS treasurer_state,
    UPPER(expn."TRES_ZIP4") AS treasurer_zip,
    CASE 
        WHEN UPPER(expn."EXPN_CODE") IN (
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
            'WEB'
        ) THEN UPPER(expn."EXPN_CODE")
        ELSE '???'
    END AS payment_code,
    expn."EXPN_DSCR" AS payment_description,
    expn."AMOUNT" AS amount,
    expn."EXPN_DATE" AS payment_date,
    expn."EXPN_CHKNO" AS check_number,
    expn."TRAN_ID" AS transaction_id,
    expn."BAKREF_TID" AS parent_transaction_id,
    expn."MEMO_REFNO" AS memo_reference_number
FROM "EXPN_CD" expn
JOIN calaccess_processed_form460version filing_version
ON expn."FILING_ID" = filing_version.filing_id
AND expn."AMEND_ID" = filing_version.amend_id
WHERE expn."FORM_TYPE" = 'E'
AND expn."MEMO_CODE" <> '';