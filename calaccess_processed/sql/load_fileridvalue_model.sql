INSERT INTO calaccess_processed_fileridvalue (table_name, column_name, value, occur_count)
SELECT 
    'BALLOT_MEASURES_CD' as table_name,
    'FILER_ID' as column_name,
    "FILER_ID"::varchar as value,
    COUNT(*) occur_count
FROM "BALLOT_MEASURES_CD"
WHERE "FILER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'CVR_CAMPAIGN_DISCLOSURE_CD' as table_name,
    'FILER_ID' as column_name,
    "FILER_ID" as value,
    COUNT(*) occur_count
FROM "CVR_CAMPAIGN_DISCLOSURE_CD"
WHERE "FILER_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'CVR_F470_CD' as table_name,
    'FILER_ID' as column_name,
    "FILER_ID" as value,
    COUNT(*) occur_count
FROM "CVR_F470_CD"
WHERE "FILER_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'CVR_LOBBY_DISCLOSURE_CD' as table_name,
    'FILER_ID' as column_name,
    "FILER_ID" as value,
    COUNT(*) occur_count
FROM "CVR_LOBBY_DISCLOSURE_CD"
WHERE "FILER_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'CVR_REGISTRATION_CD' as table_name,
    'FILER_ID' as column_name,
    "FILER_ID" as value,
    COUNT(*) occur_count
FROM "CVR_REGISTRATION_CD"
WHERE "FILER_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'CVR_SO_CD' as table_name,
     'FILER_ID' as column_name,
     "FILER_ID" as value,
     COUNT(*) occur_count
FROM "CVR_SO_CD"
WHERE "FILER_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'EFS_FILING_LOG_CD' as table_name,
     'FILER_ID' as column_name,
     "FILER_ID" as value,
     COUNT(*) occur_count
FROM "EFS_FILING_LOG_CD"
WHERE "FILER_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'F501_502_CD' as table_name,
    'FILER_ID' as column_name,
    "FILER_ID" as value,
    COUNT(*) occur_count
FROM "F501_502_CD"
WHERE "FILER_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'FILERNAME_CD' as table_name,
     'FILER_ID' as column_name,
     "FILER_ID"::varchar as value,
     COUNT(*) occur_count
FROM "FILERNAME_CD"
WHERE "FILER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'FILERS_CD' as table_name,
     'FILER_ID' as column_name,
     "FILER_ID"::varchar as value,
     COUNT(*) occur_count
FROM "FILERS_CD"
WHERE "FILER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'FILER_ACRONYMS_CD' as table_name,
     'FILER_ID' as column_name,
     "FILER_ID"::varchar as value,
     COUNT(*) occur_count
FROM "FILER_ACRONYMS_CD"
WHERE "FILER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'FILER_ADDRESS_CD' as table_name,
     'FILER_ID' as column_name,
     "FILER_ID"::varchar as value,
     COUNT(*) occur_count
FROM "FILER_ADDRESS_CD"
WHERE "FILER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'FILER_ETHICS_CLASS_CD' as table_name,
     'FILER_ID' as column_name,
     "FILER_ID"::varchar as value,
     COUNT(*) occur_count
FROM "FILER_ETHICS_CLASS_CD"
WHERE "FILER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'FILER_FILINGS_CD' as table_name,
     'FILER_ID' as column_name,
     "FILER_ID"::varchar as value,
     COUNT(*) occur_count
FROM "FILER_FILINGS_CD"
WHERE "FILER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'FILER_INTERESTS_CD' as table_name,
    'FILER_ID' as column_name,
    "FILER_ID"::varchar as value,
    COUNT(*) occur_count
FROM "FILER_INTERESTS_CD"
WHERE "FILER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'FILER_TO_FILER_TYPE_CD' as table_name,
    'FILER_ID' as column_name,
    "FILER_ID"::varchar as value,
    COUNT(*) occur_count
FROM "FILER_TO_FILER_TYPE_CD"
WHERE "FILER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'FILER_XREF_CD' as table_name,
     'FILER_ID' as column_name,
     "FILER_ID"::varchar as value,
     COUNT(*) occur_count
FROM "FILER_XREF_CD"
WHERE "FILER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'LOBBYING_CHG_LOG_CD' as table_name,
    'FILER_ID' as column_name,
    "FILER_ID"::varchar as value,
    COUNT(*) occur_count
FROM "LOBBYING_CHG_LOG_CD"
WHERE "FILER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'LOBBYIST_CONTRIBUTIONS1_CD' as table_name,
    'FILER_ID' as column_name,
    "FILER_ID"::varchar as value,
    COUNT(*) occur_count
FROM "LOBBYIST_CONTRIBUTIONS1_CD"
WHERE "FILER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'LOBBYIST_CONTRIBUTIONS2_CD' as table_name,
    'FILER_ID' as column_name,
    "FILER_ID"::varchar as value,
    COUNT(*) occur_count
FROM "LOBBYIST_CONTRIBUTIONS2_CD"
WHERE "FILER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'LOBBYIST_CONTRIBUTIONS3_CD' as table_name,
    'FILER_ID' as column_name,
    "FILER_ID"::varchar as value,
    COUNT(*) occur_count
FROM "LOBBYIST_CONTRIBUTIONS3_CD"
WHERE "FILER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'RECEIVED_FILINGS_CD' as table_name,
    'FILER_ID' as column_name,
    "FILER_ID"::varchar as value,
    COUNT(*) occur_count
FROM "RECEIVED_FILINGS_CD"
WHERE "FILER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
-- xref_ids
SELECT 
    'FILERNAME_CD' as table_name,
    'XREF_FILER_ID' as column_name,
    "XREF_FILER_ID" as value,
    COUNT(*) as occur_count
FROM "FILERNAME_CD"
WHERE "XREF_FILER_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'FILER_XREF_CD' as table_name,
    'XREF_ID' as column_name,
    'XREF_ID' as value,
    COUNT(*) as occur_count
FROM "FILER_XREF_CD"
GROUP BY 1, 2, 3
UNION ALL
-- ballot initiative (FILER_TYPE = 19) filer_ids?
SELECT 
    'CVR_CAMPAIGN_DISCLOSURE_CD' as table_name,
    'BAL_ID' as column_name,
    "BAL_ID" as value,
    COUNT(*) as occur_count
FROM "CVR_CAMPAIGN_DISCLOSURE_CD"
WHERE "BAL_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT 
    'S497_CD' as table_name, 
    'BAL_ID' as column_name,
    "BAL_ID" as value,
    COUNT(*) as occur_count
FROM "S497_CD"
WHERE "BAL_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
-- candidate/officeholder (FILER_TYPE = 8) filer_ids?
SELECT
    'CVR_CAMPAIGN_DISCLOSURE_CD' as table_name ,
    'CAND_ID' as column_name,
    "CAND_ID" as value,
    COUNT(*) as occur_count
FROM "CVR_CAMPAIGN_DISCLOSURE_CD"
WHERE "CAND_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'S497_CD' as table_name,
    'CAND_ID' as column_name,
    "CAND_ID" as value,
    COUNT(*) as occur_count
FROM "S497_CD"
WHERE "CAND_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
-- client (FILER_TYPE = 1) filer_ids?
SELECT 
    'LEMP_CD' as table_name,
    'CLIENT_ID' as column_name,
    "CLIENT_ID" as value,
    COUNT(*) as occur_count
FROM "LEMP_CD"
WHERE "CLIENT_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
-- committees includes...what?
-- recipient committee and (FILER_TYPE = 16) and
-- major donor/independent expenditure committee (FILER_TYPE = 10)?
-- maybe others?
SELECT
    'CVR_CAMPAIGN_DISCLOSURE_CD' as table_name,
    'CMTTE_ID' as column_name,
    "CMTTE_ID" as value,
    COUNT(*) as occur_count
FROM "CVR_CAMPAIGN_DISCLOSURE_CD"
WHERE "CMTTE_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'CVR2_CAMPAIGN_DISCLOSURE_CD' as table_name,
    'CMTE_ID' as column_name,
    "CMTE_ID" as value,
    COUNT(*) as occur_count
FROM "CVR2_CAMPAIGN_DISCLOSURE_CD"
WHERE "CMTE_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'CVR2_SO_CD' as table_name,
    'CMTE_ID' as column_name,
    "CMTE_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "CVR2_SO_CD"
WHERE "CMTE_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'DEBT_CD' as table_name,
    'CMTE_ID' as column_name,
    "CMTE_ID" as value,
    COUNT(*) as occur_count
FROM "DEBT_CD"
WHERE "CMTE_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'EXPN_CD' as table_name,
    'CMTE_ID' as column_name,
    "CMTE_ID" as value,
    COUNT(*) as occur_count
FROM "EXPN_CD"
WHERE "CMTE_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'F501_502_CD' as table_name,
    'COMMITTEE_ID' as column_name,
    "COMMITTEE_ID" as value,
    COUNT(*) as occur_count
FROM "F501_502_CD"
WHERE "COMMITTEE_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOAN_CD' as table_name,
    'CMTE_ID' as column_name,
    "CMTE_ID" as value,
    COUNT(*) as occur_count
FROM "LOAN_CD"
WHERE "CMTE_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'RCPT_CD' as table_name,
    'CMTE_ID' as column_name,
    "CMTE_ID" as value,
    COUNT(*) as occur_count
FROM "RCPT_CD"
WHERE "CMTE_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'S497_CD' as table_name,
    'CMTE_ID' as column_name,
    "CMTE_ID" as value,
    COUNT(*) as occur_count
FROM "S497_CD"
WHERE "CMTE_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'S498_CD' as table_name,
    'CMTE_ID' as column_name,
    "CMTE_ID" as value,
    COUNT(*) as occur_count
FROM "S498_CD"
WHERE "CMTE_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'CVR_SO_CD' as table_name,
    'COM82013ID' as column_name,
    "COM82013ID" as value,
    COUNT(*) as occur_count
FROM "CVR_SO_CD"
WHERE "COM82013ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'RCPT_CD' as table_name,
    'INTR_CMTEID' as column_name,
    "INTR_CMTEID" as value,
    COUNT(*) as occur_count
FROM "RCPT_CD"
WHERE "INTR_CMTEID" <> ''
GROUP BY 1, 2, 3
UNION ALL
-- contributors includes...what?
-- individual (FILER_TYPE = 101), payment to influence (FILER_TYPE = 5)
SELECT
    'LOBBYIST_EMPLOYER1_CD' as table_name,
    'CONTRIBUTOR_ID' as column_name,
    "CONTRIBUTOR_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_EMPLOYER1_CD"
WHERE "CONTRIBUTOR_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_EMPLOYER2_CD' as table_name,
    'CONTRIBUTOR_ID' as column_name,
    "CONTRIBUTOR_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_EMPLOYER2_CD"
WHERE "CONTRIBUTOR_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_EMPLOYER3_CD' as table_name,
    'CONTRIBUTOR_ID' as column_name,
    "CONTRIBUTOR_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_EMPLOYER3_CD"
WHERE "CONTRIBUTOR_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_EMPLOYER_HISTORY_CD' as table_name,
    'CONTRIBUTOR_ID' as column_name,
    "CONTRIBUTOR_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_EMPLOYER_HISTORY_CD"
WHERE "CONTRIBUTOR_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_FIRM1_CD' as table_name,
    'CONTRIBUTOR_ID' as column_name,
    "CONTRIBUTOR_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_FIRM1_CD"
WHERE "CONTRIBUTOR_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_FIRM2_CD' as table_name,
    'CONTRIBUTOR_ID' as column_name,
    "CONTRIBUTOR_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_FIRM2_CD"
WHERE "CONTRIBUTOR_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_FIRM3_CD' as table_name,
    'CONTRIBUTOR_ID' as column_name,
    "CONTRIBUTOR_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_FIRM3_CD"
WHERE "CONTRIBUTOR_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_FIRM_HISTORY_CD' as table_name,
    'CONTRIBUTOR_ID' as column_name,
    "CONTRIBUTOR_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_FIRM_HISTORY_CD"
WHERE "CONTRIBUTOR_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
-- employers (FILER_TYPE 2)?
SELECT
    'LOBBYIST_EMPLOYER1_CD' as table_name,
    'EMPLOYER_ID' as column_name,
    "EMPLOYER_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_EMPLOYER1_CD"
WHERE "EMPLOYER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_EMPLOYER2_CD' as table_name,
    'EMPLOYER_ID' as column_name,
    "EMPLOYER_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_EMPLOYER2_CD"
WHERE "EMPLOYER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_EMPLOYER3_CD' as table_name,
    'EMPLOYER_ID' as column_name,
    "EMPLOYER_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_EMPLOYER3_CD"
WHERE "EMPLOYER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_EMPLOYER_FIRMS1_CD' as table_name,
    'EMPLOYER_ID' as column_name,
    "EMPLOYER_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_EMPLOYER_FIRMS1_CD"
WHERE "EMPLOYER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_EMPLOYER_FIRMS2_CD' as table_name,
    'EMPLOYER_ID' as column_name,
    "EMPLOYER_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_EMPLOYER_FIRMS2_CD"
WHERE "EMPLOYER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_EMPLOYER_HISTORY_CD' as table_name,
    'EMPLOYER_ID' as column_name,
    "EMPLOYER_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_EMPLOYER_HISTORY_CD"
WHERE "EMPLOYER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_EMP_LOBBYIST1_CD' as table_name,
    'EMPLOYER_ID' as column_name,
    "EMPLOYER_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_EMP_LOBBYIST1_CD"
WHERE "EMPLOYER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_EMP_LOBBYIST2_CD' as table_name,
    'EMPLOYER_ID' as column_name,
    "EMPLOYER_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_EMP_LOBBYIST2_CD"
WHERE "EMPLOYER_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LPAY_CD' as table_name,
    'EMPLR_ID' as column_name,
    "EMPLR_ID" as value,
    COUNT(*) as occur_count
FROM "LPAY_CD"
WHERE "EMPLR_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
-- firms (FILER_TYPE 8) filer_ids?
SELECT
    'CVR_LOBBY_DISCLOSURE_CD' as table_name,
    'FIRM_ID' as column_name,
    "FIRM_ID" as value,
    COUNT(*) as occur_count
FROM "CVR_LOBBY_DISCLOSURE_CD"
WHERE "FIRM_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LEMP_CD' as table_name,
    'SUBFIRM_ID' as column_name,
    "SUBFIRM_ID" as value,
    COUNT(*) as occur_count
FROM "LEMP_CD"
WHERE "SUBFIRM_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_EMPLOYER_FIRMS1_CD' as table_name,
    'FIRM_ID' as column_name,
    "FIRM_ID"::varchar as value,
    COUNT(*)
FROM "LOBBYIST_EMPLOYER_FIRMS1_CD"
WHERE "FIRM_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_EMPLOYER_FIRMS2_CD' as table_name,
    'FIRM_ID' as column_name,
    "FIRM_ID"::varchar as value,
    COUNT(*)
FROM "LOBBYIST_EMPLOYER_FIRMS2_CD"
WHERE "FIRM_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_FIRM1_CD' as table_name,
    'FIRM_ID' as column_name,
    "FIRM_ID"::varchar as value,
    COUNT(*)
FROM "LOBBYIST_FIRM1_CD"
WHERE "FIRM_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_FIRM2_CD' as table_name,
    'FIRM_ID' as column_name,
    "FIRM_ID"::varchar as value,
    COUNT(*)
FROM "LOBBYIST_FIRM2_CD"
WHERE "FIRM_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_FIRM3_CD' as table_name,
    'FIRM_ID' as column_name,
    "FIRM_ID"::varchar as value,
    COUNT(*)
FROM "LOBBYIST_FIRM3_CD"
WHERE "FIRM_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_FIRM_EMPLOYER1_CD' as table_name,
    'FIRM_ID' as column_name,
    "FIRM_ID"::varchar as value,
    COUNT(*)
FROM "LOBBYIST_FIRM_EMPLOYER1_CD"
WHERE "FIRM_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_FIRM_EMPLOYER2_CD' as table_name,
    'FIRM_ID' as column_name,
    "FIRM_ID"::varchar as value,
    COUNT(*)
FROM "LOBBYIST_FIRM_EMPLOYER2_CD"
WHERE "FIRM_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_FIRM_HISTORY_CD' as table_name,
    'FIRM_ID' as column_name,
    "LOBBYIST_FIRM_HISTORY_CD"::varchar as value,
    COUNT(*)
FROM "LOBBYIST_FIRM_HISTORY_CD"
WHERE "LOBBYIST_FIRM_HISTORY_CD" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_FIRM_LOBBYIST1_CD' as table_name,
    'FIRM_ID' as column_name,
    "FIRM_ID"::varchar as value,
    COUNT(*)
FROM "LOBBYIST_FIRM_LOBBYIST1_CD"
WHERE "FIRM_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_FIRM_LOBBYIST2_CD' as table_name,
    'FIRM_ID' as column_name,
    "FIRM_ID"::varchar as value,
    COUNT(*)
FROM "LOBBYIST_FIRM_LOBBYIST2_CD"
WHERE "FIRM_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
-- lobbyists (FILER_TYPE 4) filer_ids?
SELECT
    'LOBBYIST_EMP_LOBBYIST1_CD' as table_name,
    'LOBBYIST_ID' as column_name,
    "LOBBYIST_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_EMP_LOBBYIST1_CD"
WHERE "LOBBYIST_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_EMP_LOBBYIST2_CD' as table_name,
    'LOBBYIST_ID' as column_name,
    "LOBBYIST_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_EMP_LOBBYIST2_CD"
WHERE "LOBBYIST_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_FIRM_LOBBYIST1_CD' as table_name,
    'LOBBYIST_ID' as column_name,
    "LOBBYIST_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_FIRM_LOBBYIST1_CD"
WHERE "LOBBYIST_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_FIRM_LOBBYIST2_CD' as table_name,
    'LOBBYIST_ID' as column_name,
    "LOBBYIST_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_FIRM_LOBBYIST2_CD"
WHERE "LOBBYIST_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
-- candidate/officeholder (FILER_TYPE 8)
SELECT
    'CVR_LOBBY_DISCLOSURE_CD' as table_name,
    'RCPCMTE_ID' as column_name,
    "RCPCMTE_ID" as value,
    COUNT(*) as occur_count
FROM "CVR_LOBBY_DISCLOSURE_CD"
WHERE "RCPCMTE_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LCCM_CD' as table_name,
    'RECIP_ID' as column_name,
    "RECIP_ID" as value,
    COUNT(*) as occur_count
FROM "LCCM_CD"
WHERE "RECIP_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_CONTRIBUTIONS1_CD' as table_name,
    'RECIPIENT_ID' as column_name,
    "RECIPIENT_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_CONTRIBUTIONS1_CD"
WHERE "RECIPIENT_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_CONTRIBUTIONS2_CD' as table_name,
    'RECIPIENT_ID' as column_name,
    "RECIPIENT_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_CONTRIBUTIONS2_CD"
WHERE "RECIPIENT_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYIST_CONTRIBUTIONS3_CD' as table_name,
    'RECIPIENT_ID' as column_name,
    "RECIPIENT_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_CONTRIBUTIONS3_CD"
WHERE "RECIPIENT_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
-- ????
SELECT
    'CVR2_LOBBY_DISCLOSURE_CD' as table_name,
    'ENTITY_ID' as column_name,
    "ENTITY_ID" as value,
    COUNT(*) as occur_count
FROM "CVR2_LOBBY_DISCLOSURE_CD"
WHERE "ENTITY_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'CVR2_REGISTRATION_CD' as table_name,
    'ENTITY_ID' as column_name,
    "ENTITY_ID" as value,
    COUNT(*) as occur_count
FROM "CVR2_REGISTRATION_CD"
WHERE "ENTITY_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'CVR_LOBBY_DISCLOSURE_CD' as table_name,
    'SENDER_ID' as column_name,
    "SENDER_ID" as value,
    COUNT(*) as occur_count
FROM "CVR_LOBBY_DISCLOSURE_CD"
WHERE "SENDER_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'CVR_REGISTRATION_CD' as table_name,
    'SENDER_ID' as column_name,
    "SENDER_ID" as value,
    COUNT(*) as occur_count
FROM "CVR_REGISTRATION_CD"
WHERE "SENDER_ID" <> ''
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'LOBBYING_CHG_LOG_CD' as table_name,
    'ENTITY_ID' as column_name,
    "ENTITY_ID"::varchar as value,
    COUNT(*) as occur_count
FROM "LOBBYING_CHG_LOG_CD"
WHERE "ENTITY_ID" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'FILER_LINKS_CD' as table_name,
    'FILER_ID_A' as column_name,
    "FILER_ID_A"::varchar as value,
    COUNT(*) as occur_count
FROM "FILER_LINKS_CD"
WHERE "FILER_ID_A" IS NOT NULL
GROUP BY 1, 2, 3
UNION ALL
SELECT
    'FILER_LINKS_CD' as table_name,
    'FILER_ID_B' as column_name,
    "FILER_ID_B"::varchar as value,
    COUNT(*) as occur_count
FROM "FILER_LINKS_CD"
WHERE "FILER_ID_B" IS NOT NULL
GROUP BY 1, 2, 3;