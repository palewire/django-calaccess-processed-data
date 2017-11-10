-- Delete any alternate CommitteeName that's equal to Committee's current name
DELETE 
FROM opencivicdata_committeename
USING opencivicdata_committee c
WHERE opencivicdata_committeename.committee_id = c.id
AND opencivicdata_committeename.name = c.name;
