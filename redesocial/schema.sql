/* Entities */
CREATE TABLE tWall(
	id_wall INTEGER NOT NULL AUTO_INCREMENT,
	PRIMARY KEY (id_wall)
);

CREATE TABLE tUser(
	id_user INTEGER NOT NULL AUTO_INCREMENT,
	id_wall INTEGER NOT NULL,
	name VARCHAR(255) NOT NULL,
	city VARCHAR(255),
	img BLOB,
	visibility INTEGER NOT NULL,
	PRIMARY KEY (id_user),
	FOREIGN KEY (id_wall) REFERENCES tWall(id_wall)
);

CREATE TABLE tGroup(
	id_group INTEGER NOT NULL AUTO_INCREMENT,
	id_wall INTEGER NOT NULL,
	name VARCHAR(255) NOT NULL,
	description VARCHAR(512),
	img BLOB,
	PRIMARY KEY (id_group),
	FOREIGN KEY (id_wall) REFERENCES tWall(id_wall)
);

CREATE TABLE tPost(
	id_post INTEGER NOT NULL AUTO_INCREMENT,
	id_user INTEGER NOT NULL,
	id_wall INTEGER NOT NULL,
	text VARCHAR(512),
	img BLOB,
	PRIMARY KEY (id_post),
	FOREIGN KEY (id_user) REFERENCES tUser(id_user),
	FOREIGN KEY (id_wall) REFERENCES tWall(id_wall)
);

CREATE TABLE tComment(
	id_comment INTEGER NOT NULL AUTO_INCREMENT,
	id_user INTEGER NOT NULL,
	id_post INTEGER NOT NULL,
	text VARCHAR(512) NOT NULL,
	PRIMARY KEY (id_comment),
	FOREIGN KEY (id_user) REFERENCES tUser(id_user),
	FOREIGN KEY (id_post) REFERENCES tPost(id_post)
);

CREATE TABLE tReply(
	id_reply INTEGER NOT NULL AUTO_INCREMENT,
	id_user INTEGER NOT NULL,
	id_comment INTEGER NOT NULL,
	text VARCHAR(512) NOT NULL,
	PRIMARY KEY (id_reply),
	FOREIGN KEY (id_user) REFERENCES tUser(id_user),
	FOREIGN KEY (id_comment) REFERENCES tComment(id_comment)
);

/* Relationships */
CREATE TABLE rUser_User(
	id_user_from INTEGER NOT NULL,
	id_user_to INTEGER NOT NULL,
	status INTEGER NOT NULL,
	PRIMARY KEY (id_user_from, id_user_to),
	FOREIGN KEY (id_user_from) REFERENCES tUser(id_user),
	FOREIGN KEY (id_user_to) REFERENCES tUser(id_user)
);

CREATE TABLE rUser_Group(
	id_user INTEGER NOT NULL,
	id_group INTEGER NOT NULL,
	status INTEGER NOT NULL,
	PRIMARY KEY (id_user, id_group),
	FOREIGN KEY (id_user) REFERENCES tUser(id_user),
	FOREIGN KEY (id_group) REFERENCES tGroup(id_group)
);
