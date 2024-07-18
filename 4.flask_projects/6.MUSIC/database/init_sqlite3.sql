-- SQLite3 데이터베이스 초기화

-- user 테이블 생성
CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- music 테이블 생성
CREATE TABLE IF NOT EXISTS music (
    music_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    album_image TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- comment 테이블 생성
CREATE TABLE IF NOT EXISTS comment (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    music_id INTEGER,
    user_id INTEGER,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (music_id) REFERENCES music(music_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
);

-- likes 테이블 생성
CREATE TABLE IF NOT EXISTS likes (
    user_id INTEGER,
    music_id INTEGER,
    liked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, music_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (music_id) REFERENCES music(music_id) ON DELETE CASCADE
);

-- notification 테이블 생성
CREATE TABLE IF NOT EXISTS notification (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    music_id INTEGER,
    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (music_id) REFERENCES music(music_id) ON DELETE CASCADE
);

-- comment 테이블에 새로운 항목이 삽입될 때 트리거
CREATE TRIGGER after_comment_insert
AFTER INSERT ON comment
FOR EACH ROW
BEGIN
    INSERT INTO notification (user_id, music_id, message)
    SELECT user_id, NEW.music_id, 'New comment added: ' || NEW.content
    FROM likes
    WHERE music_id = NEW.music_id;
END;
