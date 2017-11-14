-- join to CommitteeIdentifier to get OCD committee_id
JOIN "opencivicdata_committeeidentifier"
ON {lhs_table}."filer_id" = "opencivicdata_committeeidentifier"."identifier"::int
AND "opencivicdata_committeeidentifier"."scheme" = 'calaccess_filer_id'