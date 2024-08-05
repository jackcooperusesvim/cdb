SELECT children.id as id, 
	first_name, 
	last_name, 
	birthday, 
	family_id, 
	first_id, 
	first_hour.class_name AS first_hour_class_name, 
	second_hour.class_name AS first_hour_class_name, 
	grade_offset

FROM children 
	LEFT JOIN families 
	ON children.family_id = families.id

	LEFT JOIN first_hour
	ON children.first_id = first_hour.id

	LEFT JOIN second_hour
	ON children.second_id = second_hour.id;
