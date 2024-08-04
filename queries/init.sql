CREATE TABLE families(
	id INTEGER PRIMARY KEY,
	parent_mn TEXT NOT NULL,
	parent_sec TEXT NOT NULL,
	last_name TEXT NOT NULL,
	street TEXT NOT NULL,
	city TEXT NOT NULL,
	state TEXT NOT NULL,
	zip INTEGER NOT NULL,
	phone1 INTEGER NOT NULL,
	phone2 INTEGER NOT NULL,
	phone3 INTEGER,
	email TEXT NOT NULL,
	is_member BOOLEAN NOT NULL,
	note TEXT
);
CREATE TABLE children(
	id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	birthday TEXT NOT NULL,
	family_id INTEGER NOT NULL,
	first_id INTEGER,
	second_id INTEGER,
	grade_offset INTEGER,
	FOREIGN KEY(first_id) REFERENCES classes(id),
	FOREIGN KEY(second_id) REFERENCES classes(id),
	FOREIGN KEY(family_id) REFERENCES family(id)
);

CREATE TABLE classes(
	id INTEGER PRIMARY KEY,
	class_name TEXT UNIQUE NOT NULL,
	desc TEXT,
	hour INTEGER NOT NULL,
	member_cost INTEGER,
	regular_cost INTEGER
);
