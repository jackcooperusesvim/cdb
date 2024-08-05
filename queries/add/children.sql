INSERT INTO children(first_name,birthday,family_id,first_id,second_id,grade_offset) 
	VALUES (?, ?, ?, ?, ?, ?) 
	RETURNING id;
