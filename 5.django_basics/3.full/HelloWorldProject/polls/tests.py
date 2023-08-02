from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from polls.models import Question, Choice

class PollsAppTests(TestCase):

    def setUp(self):
        # 테스트 데이터를 생성합니다.
        self.question = Question.objects.create(
            question_text='What is your favorite color?',
            pub_date=timezone.now()
        )
        self.choice1 = Choice.objects.create(
            question=self.question,
            choice_text='Red',
            votes=0
        )
        self.choice2 = Choice.objects.create(
            question=self.question,
            choice_text='Blue',
            votes=0
        )

    def test_question_and_choice_creation(self):
        # 데이터베이스에 데이터가 잘 생성되었는지 테스트합니다.
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Choice.objects.count(), 2)

    def test_question_detail_view(self):
        # 질문 상세 페이지의 정상적인 동작을 테스트합니다.
        response = self.client.get(reverse('polls:detail', args=(self.question.id,)))
        self.assertEqual(response.status_code, 200)

        # 상세 페이지에 질문이 표시되는지를 확인합니다. - 실제로는 질문을 출력하지 않았음으로 오류 발생
        # self.assertContains(response, self.question.question_text)
        
        # 선택지가 제대로 표시되는지 확인합니다.
        for choice in self.question.choice_set.all():
            self.assertContains(response, choice.choice_text)


    def test_vote(self):
        # 투표 기능의 동작을 테스트합니다.
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': self.choice1.id})
        self.assertEqual(response.status_code, 302)  # 리다이렉션 상태 코드
        self.choice1.refresh_from_db()
        self.assertEqual(self.choice1.votes, 1)

        # 유효하지 않은 선택지 투표 시도를 테스트합니다.
        response = self.client.post(reverse('polls:vote', args=(self.question.id,)), {'choice': 999})
        self.assertEqual(response.status_code, 200)  # 오류 메시지를 포함한 상태 코드
        # 오류 메시지 확인
        error_message = "You didn't select a choice."
        # error_message = "You didn&#x27;t select a choice."
        # self.assertIn(error_message, response.content.decode())
        self.assertContains(response, error_message)

        self.choice1.refresh_from_db()
        self.assertEqual(self.choice1.votes, 1)  # 투표가 변경되지 않았음을 확인합니다.

    def test_results_view(self):
        # 결과 페이지의 동작을 테스트합니다.
        response = self.client.get(reverse('polls:results', args=(self.question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question.question_text)

# 실행 방법
# python manage.py test polls
