INSERT INTO users (username, password_hash, discord_id_hash) VALUES ('user 1', 'abc', '123');
INSERT INTO historical (user_id, record_date, pr) VALUES (2, '2023-08-11', ROW('test 1', 135.0, 175.0, 225.0));
INSERT INTO users (username, password_hash, discord_id_hash) VALUES ('user 2', 'abc', '123');
INSERT INTO historical (user_id, record_date, pr) VALUES (3, '2023-08-13', ROW('test 2', 160.0, 175.0, 225.0));
INSERT INTO users (username, password_hash, discord_id_hash) VALUES ('user 3', 'abc', '123');
INSERT INTO historical (user_id, record_date, pr) VALUES (4, '2023-08-10', ROW('test 3', 135.0, 175.0, 225.0));