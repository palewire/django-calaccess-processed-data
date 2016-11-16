INSERT INTO calaccess_processed_election (
        year,
        election_type
)        
SELECT   
        substring(scraped."name" from '[0-9]{4}') AS year,
        left(substring(scraped."name" from '[0-9]{4} (.*)'), 1) as election_type
FROM "calaccess_processed_propositionscrapedelection" AS scraped