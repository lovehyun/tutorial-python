-- 참고: flask_sqlalchemy가 자동 초기화 해줌으로 수동 초기화 불필요
-- sqlite3 database.db < init_database.sql

-- User 테이블 생성
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Tweet 테이블 생성
CREATE TABLE IF NOT EXISTS tweet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    likes_count INTEGER DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES user(id)
);

-- Like 테이블 생성
CREATE TABLE IF NOT EXISTS like (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    tweet_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(tweet_id) REFERENCES tweet(id)
);

-- 초기 사용자 삽입 (비밀번호는 단순 텍스트, 실서비스 시 암호화 필요)
INSERT INTO user (username, email, password) VALUES
('user1', 'user1@example.com', 'password1'),
('user2', 'user2@example.com', 'password2');

-- 초기 트윗 삽입
INSERT INTO tweet (content, user_id, likes_count) VALUES
('안녕하세요, 첫 트윗입니다!', 1, 0),
('두 번째 트윗이에요!', 2, 0);
