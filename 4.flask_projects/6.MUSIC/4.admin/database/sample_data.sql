-- sqlite3 music.db < sample_data.sql
-- 사용자 데이터 삽입
INSERT INTO user (username, password, email, created_at) VALUES
('admin', 'admin', 'admin@example.com', '2024-01-10 09:00:00'),
('user1', 'password1', 'user1@example.com', '2024-01-15 10:00:00'),
('user2', 'password2', 'user2@example.com', '2024-02-20 11:00:00'),
('user3', 'password3', 'user3@example.com', '2024-03-25 12:00:00');

-- 음악 데이터 삽입
INSERT INTO music (title, artist, album_image, created_at) VALUES
('Ditto', 'NewJeans', 'album.png', '2024-01-10 09:00:00'),
('VIBE (feat. Jimin of BTS)', 'TAEYANG', 'album.png', '2024-01-12 10:00:00'),
('Attention', 'NewJeans', 'album.png', '2024-01-14 11:00:00'),
('Teddy Bear', 'STAYC', 'album.png', '2024-01-18 12:00:00'),
('Pink Venom', 'BLACKPINK', 'album.png', '2024-01-20 13:00:00'),
('Shut Down', 'BLACKPINK', 'album.png', '2024-01-22 14:00:00'),
('After LIKE', 'IVE', 'album.png', '2024-01-24 15:00:00'),
('LOVE DIVE', 'IVE', 'album.png', '2024-01-26 16:00:00'),
('Hype Boy', 'NewJeans', 'album.png', '2024-01-28 17:00:00'),
('Cookie', 'NewJeans', 'album.png', '2024-01-30 18:00:00'),
('Talk that Talk', 'TWICE', 'album.png', '2024-02-02 09:00:00'),
('Forever 1', 'Girls'' Generation', 'album.png', '2024-02-04 10:00:00'),
('Feel My Rhythm', 'Red Velvet', 'album.png', '2024-02-06 11:00:00'),
('Step Back', 'GOT the beat', 'album.png', '2024-02-08 12:00:00'),
('INVU', 'TAEYEON', 'album.png', '2024-02-10 13:00:00'),
('Yours', 'JIN', 'album.png', '2024-02-12 14:00:00'),
('Yet To Come', 'BTS', 'album.png', '2024-02-14 15:00:00'),
('Good Boy Gone Bad', 'TXT', 'album.png', '2024-02-16 16:00:00'),
('Polaroid Love', 'ENHYPEN', 'album.png', '2024-02-18 17:00:00'),
('TOMBOY', '(G)I-DLE', 'album.png', '2024-02-20 18:00:00');

-- 댓글 데이터 삽입
INSERT INTO comment (music_id, user_id, content, created_at) VALUES
(1, 1, '정말 좋은 노래예요!', '2024-01-11 09:30:00'),
(1, 2, '가사가 너무 좋아요.', '2024-01-12 10:15:00'),
(2, 2, '리듬이 경쾌해서 좋아요.', '2024-01-13 11:45:00'),
(2, 3, '반복해서 듣고 있어요.', '2024-01-14 12:00:00'),
(3, 1, '목소리가 매력적이에요.', '2024-01-15 13:30:00'),
(3, 3, '추천해주셔서 들어봤는데 정말 좋네요.', '2024-01-16 14:15:00'),
(4, 2, '이 노래는 정말 최고입니다.', '2024-01-19 15:45:00'),
(4, 3, '저도 이 노래 좋아해요!', '2024-01-20 16:00:00'),
(5, 1, '계속 반복해서 듣고 있습니다.', '2024-01-21 17:30:00'),
(6, 1, '이 노래 들으면 힘이 나요.', '2024-01-23 18:15:00'),
(6, 2, '정말 감동적인 노래예요.', '2024-01-24 19:45:00'),
(7, 3, '가창력이 대단해요.', '2024-01-25 20:00:00'),
(8, 2, '이 노래는 언제 들어도 좋아요.', '2024-01-27 21:30:00'),
(9, 1, '멜로디가 인상적입니다.', '2024-01-29 22:15:00'),
(10, 3, '친구에게 추천받아서 들었어요.', '2024-01-31 23:45:00'),
(10, 2, '정말 추천할 만한 곡입니다.', '2024-02-01 00:00:00'),
(11, 1, '이 노래를 들으면 기분이 좋아져요.', '2024-02-03 09:30:00'),
(12, 3, '리듬이 너무 좋아요.', '2024-02-05 10:15:00'),
(13, 2, '자주 듣고 있어요.', '2024-02-07 11:45:00'),
(14, 1, '이 노래는 정말 대단해요.', '2024-02-09 12:00:00'),
(15, 2, '들으면 들을수록 좋네요.', '2024-02-11 13:30:00'),
(16, 3, '이 노래는 정말 명곡입니다.', '2024-02-13 14:15:00'),
(17, 1, '가사가 정말 좋아요.', '2024-02-15 15:45:00'),
(18, 2, '목소리가 너무 좋아요.', '2024-02-17 16:00:00'),
(19, 3, '자꾸 생각나는 노래입니다.', '2024-02-19 17:30:00'),
(20, 1, '이 노래를 들으면 기분이 좋아져요.', '2024-02-21 18:15:00');

-- 해시태그 데이터 삽입
INSERT INTO hashtag (tag) VALUES
('Kpop'),
('Pop'),
('Dance'),
('Ballad'),
('HipHop'),
('R&B'),
('Rock'),
('Indie'),
('Electronic'),
('Folk');

-- 음악-해시태그 관계 데이터 삽입
-- Ditto
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(1, 1), (1, 3);

-- VIBE (feat. Jimin of BTS)
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(2, 1), (2, 5), (2, 6);

-- Attention
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(3, 1);

-- Teddy Bear
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(4, 1), (4, 3), (4, 8);

-- Pink Venom
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(5, 1), (5, 3);

-- Shut Down
-- 해시태그 없음

-- After LIKE
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(7, 1), (7, 2);

-- LOVE DIVE
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(8, 1), (8, 2), (8, 7);

-- Hype Boy
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(9, 1), (9, 3);

-- Cookie
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(10, 1), (10, 3), (10, 5);

-- Talk that Talk
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(11, 1), (11, 2);

-- Forever 1
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(12, 1), (12, 2), (12, 4);

-- Feel My Rhythm
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(13, 1), (13, 2);

-- Step Back
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(14, 1), (14, 3), (14, 6);

-- INVU
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(15, 1), (15, 4);

-- Yours
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(16, 1);

-- Yet To Come
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(17, 1), (17, 2);

-- Good Boy Gone Bad
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(18, 1), (18, 5);

-- Polaroid Love
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(19, 1), (19, 3);

-- TOMBOY
INSERT INTO music_hashtag (music_id, hashtag_id) VALUES
(20, 1), (20, 3), (20, 5);
