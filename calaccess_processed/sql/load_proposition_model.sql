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
  JOIN calaccess_processed_propositionscrapedelection AS scrapedelection
    ON scraped.election_id = scrapedelection.id
  JOIN calaccess_processed_election AS election
    ON substring(scrapedelection.name from '\d{4}')::INT = election.year
   AND substring(scrapedelection.name from '\d{4}\s([A-Z])') = election.election_type;
   