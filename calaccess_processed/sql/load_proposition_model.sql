INSERT INTO calaccess_processed_proposition (
            id,
            name,
            election_id
    )
SELECT
        scraped.scraped_id::INTEGER AS id,
        scraped.name AS name,
        election.id AS election_id
  FROM calaccess_processed_scrapedproposition AS scraped
  JOIN (
        SELECT id,
               substring(name from '\d{4}\s([A-Z])') AS election_type,
               (regexp_matches(name, '^([A-Z]+\s\d{1,2},\s\d{4})\s.+$'))[1]::DATE as election_date
        FROM calaccess_processed_propositionscrapedelection
       ) AS scrapedelection
    ON scraped.election_id = scrapedelection.id
  JOIN calaccess_processed_election AS election
    ON left(election.election_type, 1) = scrapedelection.election_type
   AND election.election_date = scrapedelection.election_date
ORDER BY id;
