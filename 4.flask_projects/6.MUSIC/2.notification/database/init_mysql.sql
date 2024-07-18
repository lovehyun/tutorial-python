-- MySQL 데이터베이스 초기화

-- user 테이블 생성
CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- music 테이블 생성
CREATE TABLE IF NOT EXISTS music (
    music_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    artist VARCHAR(100) NOT NULL,
    album_image VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- comment 테이블 생성
CREATE TABLE IF NOT EXISTS comment (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    music_id INT,
    user_id INT,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (music_id) REFERENCES music(music_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
);

-- likes 테이블 생성
CREATE TABLE IF NOT EXISTS likes (
    user_id INT,
    music_id INT,
    liked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, music_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (music_id) REFERENCES music(music_id) ON DELETE CASCADE
);

-- notification 테이블 생성
CREATE TABLE IF NOT EXISTS notification (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    music_id INT,
    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (music_id) REFERENCES music(music_id) ON DELETE CASCADE
);

-- DELIMITER 설정
DELIMITER //

-- comment 테이블에 새로운 항목이 삽입될 때 트리거
CREATE TRIGGER after_comment_insert
AFTER INSERT ON comment
FOR EACH ROW
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE liked_user_id INT;
    DECLARE cur CURSOR FOR SELECT user_id FROM likes WHERE music_id = NEW.music_id;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO liked_user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        INSERT INTO notification (user_id, music_id, message)
        VALUES (liked_user_id, NEW.music_id, CONCAT('New comment added: ', NEW.content));

    END LOOP;

    CLOSE cur;
END//

-- DELIMITER 원래대로 복원
DELIMITER ;
