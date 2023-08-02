from django.db import models

class Question(models.Model):
    # question_text: 설문 조사 질문 내용을 담을 필드로, 
    #   CharField 타입으로 최대 길이가 200인 문자열을 저장합니다.
    # pub_date: 설문 조사를 발행한 날짜와 시간을 담을 필드로, 
    #   DateTimeField 타입으로 사용됩니다. 
    #   'date published'라는 이름으로 설명이 추가되어 있습니다.
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    
class Choice(models.Model):
    # question: Question 모델과의 관계를 나타내는 외래키(ForeignKey) 필드입니다. 
    #   각 Choice 객체는 Question 모델의 특정 질문과 연결됩니다. 
    #   on_delete=models.CASCADE 옵션은 연결된 Question이 삭제되면 해당 Choice 레코드도 함께 삭제됨을 의미합니다.
    # choice_text: 선택지 내용을 담을 필드로, 
    #   CharField 타입으로 최대 길이가 200인 문자열을 저장합니다.
    # votes: 선택지에 대한 투표 수를 담을 필드로, 
    #   IntegerField 타입으로 기본값이 0으로 설정되어 있습니다.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
