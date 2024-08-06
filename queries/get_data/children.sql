SELECT children.id as id, 
	first_name, 
	CONCAT(last_name,'|',family_id) AS family,
	CONCAT(first_hour.class_name,'|',first_id) AS first_hour,
	CONCAT(second_hour.class_name,'|',second_id) AS second_hour,
	birthday, 
	grade_offset

FROM children 
	LEFT JOIN families 
	ON children.family_id = families.id

	LEFT JOIN first_hour
	ON children.first_id = first_hour.id

	LEFT JOIN second_hour
	ON children.second_id = second_hour.id;
