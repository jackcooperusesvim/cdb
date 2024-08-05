INSERT INTO first_hour(class_name,desc,member_cost,regular_cost) 
	VALUES (? ,? ,? ,?)
	RETURNING id;
