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
	is_member TEXT NOT NULL,
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
	FOREIGN KEY(first_id) REFERENCES first_hour(id),
	FOREIGN KEY(second_id) REFERENCES second_hour(id),
	FOREIGN KEY(family_id) REFERENCES families(id)
);

CREATE TABLE first_hour(
	id INTEGER PRIMARY KEY,
	class_name TEXT UNIQUE NOT NULL,
	desc TEXT,
	member_cost INTEGER,
	regular_cost INTEGER
);
CREATE TABLE second_hour(
	id INTEGER PRIMARY KEY,
	class_name TEXT UNIQUE NOT NULL,
	desc TEXT,
	member_cost INTEGER,
	regular_cost INTEGER
);
