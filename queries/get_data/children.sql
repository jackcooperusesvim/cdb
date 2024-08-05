SELECT children.id as id, 
	first_name, 
	last_name, 
	CONCAT(family_id,'|',last_name),
	CONCAT(first_id,'|',first_hour.class_name),
	CONCAT(second_id,'|',second_hour.class_name),
	birthday, 
	grade_offset

FROM children 
	LEFT JOIN families 
	ON children.family_id = families.id

	LEFT JOIN first_hour
	ON children.first_id = first_hour.id

	LEFT JOIN second_hour
	ON children.second_id = second_hour.id;
