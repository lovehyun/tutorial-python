from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings
from .models import Photo
import os

class PhotoUploadTests(TestCase):
    def test_photo_upload_view(self):
        # 사진 업로드 페이지로의 접속 테스트
        response = self.client.get(reverse('photo_upload'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photo_upload/photo_upload.html')

    @override_settings(MEDIA_ROOT='./upload/test_media/')  # 테스트용 MEDIA_ROOT 설정
    def test_photo_upload(self):
        # 사진 업로드 테스트 - 적절한 테스트 경로로 설정
        with open('/path/to/image.jpg', 'rb') as file:
            response = self.client.post(reverse('photo_upload'), {'title': 'Test Photo', 'image': file})
        
        self.assertEqual(response.status_code, 302)  # 업로드 후 리다이렉션 상태 코드

        # 업로드 된 사진이 Photo 모델에 추가되었는지 확인
        self.assertEqual(Photo.objects.count(), 1)
        photo = Photo.objects.first()

        # 파일이 올바른 경로에 저장되었는지 확인
        expected_file_path = os.path.join(settings.MEDIA_ROOT, '/photos/', 'image.jpg')
        self.assertTrue(os.path.exists(expected_file_path))

        # 파일 URL이 'MEDIA_URL'을 포함하고 있는지 확인
        self.assertTrue(photo.image.url.startswith(settings.MEDIA_URL))

    def test_photo_list_view(self):
        # 사진 목록 페이지 테스트
        response = self.client.get(reverse('photo_list'))
        # print(response.content.decode())  # 페이지의 HTML 내용 출력
        self.assertEqual(response.status_code, 200)  # 페이지가 정상적으로 로딩되는지 확인
        self.assertContains(response, 'Photo List')  # 페이지에 'Photo List'가 포함되는지 확인
