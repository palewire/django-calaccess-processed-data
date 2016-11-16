INSERT INTO calaccess_processed_propositioncommittee (
        committee_filer_id,
        name,
        proposition_id,
        position
)        
SELECT   
        committee."scraped_id"::INTEGER AS committee_filerid,
        committee."name" AS name,
        proposition."scraped_id"::INTEGER AS proposition_id,
        left(committee."position", 1) AS position
FROM "calaccess_processed_scrapedpropositioncommittee" AS committee
JOIN "calaccess_processed_scrapedproposition" proposition
ON committee."proposition_id" = proposition.id