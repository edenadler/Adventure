CREATE TABLE adventures (name varchar(20), 
id MEDIUMINT AUTO_INCREMENT NOT NULL, 
PRIMARY KEY (id));

ALTER TABLE adventures
ADD current_step integer;

ALTER TABLE adventures
ADD adventure_id integer;

RENAME TABLE adventures TO userinfo;

ALTER TABLE userinfo
ADD score integer;

ALTER TABLE userinfo DROP PRIMARY KEY, ADD PRIMARY KEY(id, adventure_id);

CREATE TABLE questions (question varchar(140),
question_number int NOT NULL, 
adventure_id int NOT NULL, 
PRIMARY KEY (question_number),
FOREIGN KEY (adventure_id) REFERENCES userinfo(adventure_id));

INSERT INTO userinfo
VALUES ("eden", 100,1,1,50);