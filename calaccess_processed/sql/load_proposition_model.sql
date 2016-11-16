INSERT INTO calaccess_processed_proposition (
        id,
        name
)        
SELECT   
        scraped."scraped_id"::INTEGER AS proposition_id,
        scraped."name" as name
FROM "calaccess_processed_scrapedproposition" AS scraped