INSERT INTO calaccess_processed_proposition (
        id,
        name,
        election_id
)        
SELECT   
        scraped."scraped_id"::INTEGER AS id,
        scraped."name" as name,
        election."id" as election_id
FROM "calaccess_processed_scrapedproposition" AS scraped
JOIN "calaccess_processed_propositionscrapedelection" AS scrapedelection
ON scraped."election_id" = scrapedelection."id"
JOIN "calaccess_processed_election" AS election
ON substring(scrapedelection."name" from '[0-9]{4}') = election."year" AND
   left(substring(scrapedelection."name" from '[0-9]{4} (.*)'), 1) = election."election_type"