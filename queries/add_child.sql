INSERT INTO children(first_name, birth_year, birth_month, birth_day, grade_offset , first_id, second_id)
	VALUES (? ,? ,? ,? ,? ,? ,?)
	RETURNING id;

