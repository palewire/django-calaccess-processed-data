INSERT INTO calaccess_processed_election (
            year,
            election_type
        )        
SELECT DISTINCT   
        substring(scraped.name from '[0-9]{4}') AS year,
        -- first letter corresponds to election type
        left(substring(scraped.name from '[0-9]{4} (.*)'), 1) as election_type
  FROM calaccess_processed_candidatescrapedelection AS scraped;