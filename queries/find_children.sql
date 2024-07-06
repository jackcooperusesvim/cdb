SELECT children.id, first_name FROM children 
	LEFT JOIN families 
	ON children.family_id = families.id
	WHERE families.id = ?;
