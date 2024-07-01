CREATE TABLE families(
	id INTEGER PRIMARY KEY,
	parent_mn TEXT NOT NULL,
	parent_sec TEXT NOT NULL,
	last_name TEXT NOT NULL,
	street TEXT NOT NULL UNIQUE,
	city TEXT NOT NULL,
	state TEXT NOT NULL,
	zip INTEGER NOT NULL,
	phone1 INTEGER NOT NULL,
	phone2 INTEGER NOT NULL,
	phone3 INTEGER,
	email TEXT NOT NULL,
	is_member BOOLEAN NOT NULL,
	noteTEXT
);
CREATE TABLE children(
	id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	birth_year INTEGER NOT NULL,
	birth_month INTEGER NOT NULL,
	birth_day INTEGER NOT NULL,
	grade_offset INTEGER,
	first_id INTEGER,
	second_id INTEGER,
	FOREIGN KEY(first_id) REFERENCES classes(id),
	FOREIGN KEY(second_id) REFERENCES classes(id)
);

CREATE TABLE classes(
	id INTEGER PRIMARY KEY,
	name TEXT UNIQUE NOT NULL,
	desc TEXT,
	HOUR INTEGER NOT NULL,
	member_cost INTEGER,
	regular_cost INTEGER
);

CREATE TABLE childrenfamily(
	id INTEGER PRIMARY KEY,
	family_id INTEGER,
	child_id INTEGER,
	UNIQUE(family_id, child_id),
	FOREIGN KEY (family_id) REFERENCES families(id),
	FOREIGN KEY (child_id) REFERENCES children(id)
);
