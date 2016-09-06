INSERT INTO calaccess_processed_filingidvalue (table_name, value, occur_count)
SELECT 
    'CVR2_CAMPAIGN_DISCLOSURE_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "CVR2_CAMPAIGN_DISCLOSURE_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'CVR2_LOBBY_DISCLOSURE_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "CVR2_LOBBY_DISCLOSURE_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'CVR2_REGISTRATION_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "CVR2_REGISTRATION_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'CVR2_SO_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "CVR2_SO_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'CVR3_VERIFICATION_INFO_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "CVR3_VERIFICATION_INFO_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'CVR_CAMPAIGN_DISCLOSURE_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "CVR_CAMPAIGN_DISCLOSURE_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'CVR_E530_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "CVR_E530_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'CVR_F470_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "CVR_F470_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'CVR_LOBBY_DISCLOSURE_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "CVR_LOBBY_DISCLOSURE_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'CVR_REGISTRATION_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "CVR_REGISTRATION_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'CVR_SO_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "CVR_SO_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'DEBT_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "DEBT_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'EXPN_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "EXPN_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'F495P2_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "F495P2_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'F501_502_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "F501_502_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'F690P2_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "F690P2_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'HDR_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "HDR_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'LATT_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "LATT_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'LCCM_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "LCCM_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'LEMP_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "LEMP_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'LEXP_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "LEXP_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'LOAN_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "LOAN_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'LOBBYIST_FIRM_EMPLOYER1_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_FIRM_EMPLOYER1_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'LOBBYIST_FIRM_EMPLOYER2_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "LOBBYIST_FIRM_EMPLOYER2_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'LOBBY_AMENDMENTS_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "LOBBY_AMENDMENTS_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'LOTH_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "LOTH_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'LPAY_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "LPAY_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'RCPT_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "RCPT_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'RECEIVED_FILINGS_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "RECEIVED_FILINGS_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'S401_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "S401_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'S496_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "S496_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'S497_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "S497_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'S498_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "S498_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'SMRY_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "SMRY_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'SPLT_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "SPLT_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2
UNION ALL
SELECT 
    'TEXT_MEMO_CD' as table_name,
    "FILING_ID" as value,
    COUNT(*) as occur_count
FROM "TEXT_MEMO_CD"
WHERE "FILING_ID" IS NOT NULL
GROUP BY 1, 2;