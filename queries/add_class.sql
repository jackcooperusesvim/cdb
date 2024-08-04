INSERT INTO classes(class_name,desc,hour,member_cost, regular_cost) 
	VALUES (?, ?, ?, ?, ?) 
	RETURNING id;
