INSERT INTO families(parent_mn, parent_sec, last_name, street, city, state, zip, phone1, phone2, phone3, email, is_member, note) 
	VALUES (? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?)
	RETURNING id;
