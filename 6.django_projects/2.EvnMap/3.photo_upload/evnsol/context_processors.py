from django.conf import settings

# 동적 URL 처리를 위한 경로 생성함수
def url_prefix(request):
    web_url_prefix = ''
    url_prefix = settings.URL_PREFIX

    if len(url_prefix):
        web_url_prefix = settings.URL_PREFIX.strip('/')
        web_url_prefix = '/' + web_url_prefix

    return {'WEB_URL_PREFIX': web_url_prefix}
