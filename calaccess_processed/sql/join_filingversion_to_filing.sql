-- join FilingVersion model table to Filing model table
JOIN {rhs_table}
ON {lhs_table}."filing_version_id" = {rhs_table}."id"