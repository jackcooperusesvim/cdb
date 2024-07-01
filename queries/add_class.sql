INSERT INTO classes(name,desc,hour,member_cost, regular_cost) 
	VALUES (?, ?, ?, ?, ?) 
	RETURNING id;
