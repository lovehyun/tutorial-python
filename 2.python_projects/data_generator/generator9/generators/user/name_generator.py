import random

from generators.generator import Generator


class NameGenerator(Generator):
    def __init__(self):
        # https://ko.wikipedia.org/wiki/%ED%95%9C%EA%B5%AD%EC%9D%98_%EC%84%B1%EC%94%A8%EC%99%80_%EC%9D%B4%EB%A6%84
        self.last_names = ['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임']
        self.first_names = ['유진', '민지', '수빈', '지원', '지현', '지은', '현지', '은지', '예진', '예지', 
                            '동현', '지훈', '성민', '현우', '준호', '민석', '민수', '준혁', '준영', '승현',
                            '서아', '이서', '하윤', '지아', '지안', '서윤', '아린', '아윤', '하은', '하린',
                            '서준', '도윤', '하준', '은우', '시우', '지호', '예준', '수호', '유준', '이안']

    def generate(self):
        last_name = random.choice(self.last_names)
        first_name = random.choice(self.first_names)
        return last_name + first_name
