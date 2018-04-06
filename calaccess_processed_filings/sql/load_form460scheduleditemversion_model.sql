INSERT INTO calaccess_processed_filings_form460scheduleditemversion (
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
    cumulative_ytd_amount,
    cumulative_election_amount,
    expense_date,
    check_number,
    transaction_id,
    memo_reference_number,
    support_oppose_code,
    ballot_measure_jurisdiction,
    ballot_measure_name,
    ballot_measure_num,
    candidate_district,
    candidate_jurisdiction_code,
    candidate_jurisdiction_description,
    candidate_title,
    candidate_firstname,
    candidate_lastname,
    candidate_name_suffix,
    office_code,
    office_description,
    office_sought_held
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
            'SCC',
            ''
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
            'WEB',
            ''
        ) THEN UPPER(expn."EXPN_CODE")
        ELSE '???'
    END AS payment_code,
    expn."EXPN_DSCR" AS payment_description,
    expn."AMOUNT" AS amount,
    expn."CUM_YTD" AS cumulative_ytd_amount,
    expn."CUM_OTH" AS cumulative_election_amount,
    expn."EXPN_DATE" AS expense_date,
    expn."EXPN_CHKNO" AS check_number,
    expn."TRAN_ID" AS transaction_id,
    expn."MEMO_REFNO" AS memo_reference_number,
    CASE
        WHEN UPPER(expn."SUP_OPP_CD") IN (
            'S',
            'O',
            ''
        ) THEN UPPER(expn."SUP_OPP_CD")
        ELSE '?'
    END AS support_oppose_code,
    UPPER(expn."BAL_JURIS") AS ballot_measure_jurisdiction,
    UPPER(expn."BAL_NAME") AS ballot_measure_name,
    UPPER(expn."BAL_NUM") AS ballot_measure_num,
    UPPER(expn."DIST_NO") AS candidate_district,
    CASE
        WHEN UPPER(expn."JURIS_CD") IN (
            'ASM',
            'BOE',
            'CIT',
            'CTY',
            'LOC',
            'OTH',
            'SEN',
            'STW',
            ''
        ) THEN UPPER(expn."JURIS_CD")
        ELSE '???'
    END AS candidate_jurisdiction_code,
    UPPER(expn."JURIS_DSCR") AS candidate_jurisdiction_description,
    UPPER(expn."CAND_NAMT") AS candidate_title,
    UPPER(expn."CAND_NAMF") AS candidate_firstname,
    UPPER(expn."CAND_NAML") AS candidate_lastname,
    UPPER(expn."CAND_NAMS") AS candidate_name_suffix,
    CASE
        WHEN UPPER(expn."OFFICE_CD") IN (
            'APP',
            'ASM',
            'ASR',
            'ATT',
            'BED',
            'BOE',
            'BSU',
            'CAT',
            'CCB',
            'CCM',
            'CON',
            'COU',
            'CSU',
            'CTR',
            'DAT',
            'GOV',
            'INS',
            'LTG',
            'MAY',
            'OTH',
            'PDR',
            'PER',
            'PLN',
            'SCJ',
            'SEN',
            'SHC',
            'SOS',
            'SPM',
            'SUP',
            'TRE',
            'TRS',
            ''
        ) THEN UPPER(expn."OFFICE_CD")
        WHEN UPPER(expn."OFFICE_CD") = 'LEG' THEN 'ASM'
        WHEN UPPER(expn."OFFICE_CD") = 'OF' THEN 'ASM'
        WHEN UPPER(expn."OFFICE_CD") = 'REP' THEN 'ASM'
        WHEN UPPER(expn."OFFICE_CD") = '05' THEN 'ASM'
        ELSE '???'
    END AS office_code,
    UPPER(expn."OFFIC_DSCR") AS office_description,
    CASE
        WHEN UPPER(expn."OFF_S_H_CD") IN (
            'S',
            'H',
            ''
        ) THEN UPPER(expn."OFF_S_H_CD")
        ELSE '?'
    END AS office_sought_held
FROM "EXPN_CD" expn
JOIN calaccess_processed_filings_form460filingversion filing_version
ON expn."FILING_ID" = filing_version.filing_id
AND expn."AMEND_ID" = filing_version.amend_id
WHERE expn."FORM_TYPE" = 'D'
AND expn."MEMO_CODE" = '';
