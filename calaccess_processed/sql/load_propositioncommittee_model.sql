-- Create list of unique committees
INSERT INTO calaccess_processed_propositioncommittee (
        id,
        name
)        
SELECT
	committee."scraped_id"::INTEGER AS id,
	MIN(committee."name") AS name
FROM "calaccess_processed_scrapedpropositioncommittee" AS committee
GROUP BY committee."scraped_id";

-- Add links between committees and propositions they support and oppose
INSERT INTO calaccess_processed_propositionsupportoppose (
	committee_id,
	proposition_id,
	support_oppose
)
SELECT
	committee."scraped_id"::INTEGER AS committee_id,
	proposition."scraped_id"::INTEGER AS proposition_id,
	left(committee."position",1) AS support_oppose
FROM "calaccess_processed_scrapedpropositioncommittee" AS committee
JOIN "calaccess_processed_scrapedproposition" AS proposition
ON committee."proposition_id" = proposition."id";