## DB를 사용한 데이터 저장
데이터베이스를 사용하기 위해서는 모델을 정의하고, 이를 데이터베이스에 매핑하여 데이터를 저장하고 조회하는 과정이 필요합니다.

### 앱 개발
예제를 위해 "HelloWorldProject" 프로젝트 내에 "helloworldapp" 앱을 사용하겠습니다.

1. 모델 정의하기:
   
    helloworldapp/models.py 파일에 다음과 같이 모델을 정의합니다. 이 예제에서는 간단한 메시지를 저장하는 모델인 Message를 만들어보겠습니다.
    ```
    from django.db import models

    class Message(models.Model):
        text = models.CharField(max_length=200)

        def __str__(self):
            return self.text
    ```

2. 데이터베이스에 모델 적용하기:
   
    프로젝트 폴더로 이동한 뒤, 다음 명령을 실행하여 모델을 데이터베이스에 적용합니다.
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

3. 데이터 생성하기:
   
    장고 쉘을 실행하여 데이터베이스에 데이터를 생성해보겠습니다.
    ```
    python manage.py shell
    ```

    ```
    # 쉘에서 다음과 같이 데이터를 생성합니다.
    from helloworldapp.models import Message
    message = Message(text="안녕하세요, Django!")
    message.save()
    ```

4. 데이터 조회하기:
   
    데이터베이스에 저장된 메시지를 조회해봅니다.
    ```
    python manage.py shell
    ```

    ```
    # 쉘에서 다음과 같이 데이터를 조회합니다.
    from helloworldapp.models import Message
    messages = Message.objects.all()
    for message in messages:
        print(message.text)
    ```

    위의 예제를 따라하면, 간단한 모델을 정의하고 데이터베이스에 데이터를 생성하고 조회하는 과정을 확인할 수 있습니다. Django에서 데이터베이스를 다루는 작업은 모델을 정의하여 데이터베이스 테이블과 매핑하는 방식으로 이루어집니다. 이를 통해 데이터를 쉽고 효율적으로 관리할 수 있습니다.

5. 데이터 삭제하기
    ```
    # 삭제할 데이터 객체 가져오기
    message_to_delete = Message.objects.get(id=1)  # 여기서 'id=1'은 삭제할 메시지의 primary key입니다.

    # 데이터 삭제
    message_to_delete.delete()
    ```

    또는 메세지 아이디를 모를 경우에는...
    
    ```
    # text 필드가 "삭제할 메시지"인 모든 데이터 삭제
    messages_to_delete = Message.objects.filter(text="삭제할 메시지")
    messages_to_delete.delete()
    ```
