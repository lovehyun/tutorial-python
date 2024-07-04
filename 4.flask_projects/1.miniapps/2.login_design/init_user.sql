-- sqlite3 users.db < init_user.sql

-- create_user_table.sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- insert_user.sql
INSERT INTO users (username, password) VALUES ('username', 'password');
