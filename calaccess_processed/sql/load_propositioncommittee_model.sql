-- Create unique list of committees
INSERT INTO calaccess_processed_propositioncommittee (
        id,
        name
)        
SELECT
	committee."scraped_id"::INTEGER AS id,
	MIN(committee."name") AS name
FROM "calaccess_processed_scrapedpropositioncommittee" AS committee
GROUP BY committee."scraped_id"

-- Add links between committees and propositions they support
INSERT INTO calaccess_processed_propositioncommittee_supports (
	propositioncommittee_id,
	proposition_id
)
SELECT
	committee."scraped_id"::INTEGER AS propositioncommittee_id,
	proposition."scraped_id"::INTEGER AS proposition_id
FROM "calaccess_processed_scrapedpropositioncommittee" AS committee
JOIN "calaccess_processed_scrapedproposition" AS proposition
ON committee."proposition_id" = proposition."id"
WHERE committee."position" = 'SUPPORT'

-- Add links between committees and propositions they oppose
INSERT INTO calaccess_processed_propositioncommittee_opposes (
	propositioncommittee_id,
	proposition_id
)
SELECT
	committee."scraped_id"::INTEGER AS propositioncommittee_id,
	proposition."scraped_id"::INTEGER AS proposition_id
FROM "calaccess_processed_scrapedpropositioncommittee" AS committee
JOIN "calaccess_processed_scrapedproposition" AS proposition
ON committee."proposition_id" = proposition."id"
WHERE committee."position" = 'OPPOSE'