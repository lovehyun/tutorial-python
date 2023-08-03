from django.test import TestCase
from django.urls import reverse
from .models import Task

# TaskModelTests: 이 테스트 클래스는 models.py 파일에 정의된 Task 모델을 테스트하는데 사용됩니다. 
#   이 클래스에는 test_str_representation라는 하나의 테스트 메서드가 있습니다. 
#   이 메서드는 Task 객체의 문자열 표현을 테스트합니다. 특정 제목과 설명을 가진 Task 객체를 생성하고, 
#   이 객체의 문자열 표현이 기대하는 값과 일치하는지 assertEqual 메서드를 사용하여 확인합니다. 
#   이렇게 함으로써 Task 모델의 __str__ 메서드가 올바르게 작동하는지 확인합니다.
class TaskModelTests(TestCase):
    def test_str_representation(self):
        task = Task.objects.create(title='Test Task', description='This is a test task')
        self.assertEqual(str(task), 'Test Task')


# TaskViewTests: 이 테스트 클래스는 views.py 파일에 있는 뷰들을 테스트하는데 사용됩니다. 
#   다양한 뷰 함수를 각각 다른 테스트 메서드로 포함하고 있습니다.
class TaskViewTests(TestCase):
    # a. test_task_list_view: 이 메서드는 task_list 뷰를 테스트합니다. 
    #    Django의 client를 사용하여 task_list 뷰에 대한 GET 요청을 생성하고, reverse 함수를 사용하여 뷰의 URL을 생성합니다. 
    #    그런 다음, assertEqual 및 assertTemplateUsed와 같은 다양한 assertion을 사용하여 응답이 성공적인지(상태 코드 200) 및 올바른 템플릿이 사용되었는지 확인합니다.
    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_list.html')

    # b. test_task_detail_view: 이 메서드는 task_detail 뷰를 테스트합니다. 
    #    이전 메서드와 유사하게 client를 사용하여 task_detail 뷰에 대한 GET 요청을 생성하고, Task 객체의 기본 키(pk)를 전달합니다. 
    #    그런 다음 assertion을 사용하여 응답이 성공적인지, 올바른 템플릿이 사용되었는지, 
    #    응답이 기대하는 내용(제목과 설명)을 포함하는지 확인합니다.
    def test_task_detail_view(self):
        task = Task.objects.create(title='Test Task', description='This is a test task')
        response = self.client.get(reverse('task_detail', args=(task.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_detail.html')
        self.assertContains(response, 'Test Task')
        self.assertContains(response, 'This is a test task')

    # c. test_task_create_view: 
    #    이 메서드는 task_create 뷰를 테스트합니다. 
    #    먼저 task_create 뷰에 대한 GET 요청을 생성하여 올바른 템플릿이 렌더링되는지 확인합니다. 
    #    그런 다음, 새로운 Task 객체를 생성하기 위해 필요한 데이터가 들어 있는 딕셔너리 data를 작성합니다. 
    #    이 데이터를 사용하여 task_create 뷰에 POST 요청을 생성하고, 
    #    응답이 성공적인지(상태 코드 302) 및 데이터베이스에 새로운 Task 객체가 생성되었는지 확인합니다.
    def test_task_create_view(self):
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_create.html')

        data = {
            'title': 'New Task',
            'description': 'This is a new task',
        }
        response = self.client.post(reverse('task_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)

    # d. test_task_update_view: 이 메서드는 task_update 뷰를 테스트합니다. 
    #    이전 메서드와 마찬가지로, 먼저 task_update 뷰에 대한 GET 요청을 생성하여 올바른 템플릿이 렌더링되는지 확인합니다. 
    #    그런 다음, 데이터베이스에 Task 객체를 생성합니다. 업데이트할 Task 객체에 대한 새로운 데이터가 포함된 딕셔너리 data를 작성합니다. 
    #    이 데이터와 Task 객체의 기본 키(pk)를 사용하여 task_update 뷰에 POST 요청을 생성하고, 
    #    응답이 성공적인지, 데이터베이스의 Task 객체가 새 데이터로 업데이트되었는지, 
    #    그리고 올바른 템플릿이 사용되었는지 확인합니다.
    def test_task_update_view(self):
        task = Task.objects.create(title='Test Task', description='This is a test task')
        response = self.client.get(reverse('task_update', args=(task.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_update.html')
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'This is a test task')

        data = {
            'title': 'Updated Task',
            'description': 'This is an updated task',
        }
        response = self.client.post(reverse('task_update', args=(task.pk,)), data)
        self.assertEqual(response.status_code, 302)

        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Task')
        self.assertEqual(task.description, 'This is an updated task')

    # e. test_task_delete_view: 이 메서드는 task_delete 뷰를 테스트합니다. 
    #    이전 메서드와 유사하게, 데이터베이스에 Task 객체를 생성합니다. 
    #    그런 다음 Task 객체의 기본 키(pk)를 사용하여 task_delete 뷰에 POST 요청을 생성합니다. 
    #    그리고 응답이 성공적인지(상태 코드 302) 및 데이터베이스에서 Task 객체가 삭제되었는지 확인합니다.
    def test_task_delete_view(self):
        task = Task.objects.create(title='Test Task', description='This is a test task')
        self.assertEqual(Task.objects.count(), 1)
        
        response = self.client.post(reverse('task_delete', args=(task.pk,)))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)

# 실행 방법
# python manage.py test todo
