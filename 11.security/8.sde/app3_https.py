# openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes
# key.pem: 비공개 키 파일
# cert.pem: 인증서 파일

# Windows에서 OpenSSL 환경 변수가 설정되지 않았다면, OpenSSL 설치 디렉토리로 이동하여 openssl.exe를 직접 실행하거나, 설치 디렉토리를 PATH에 추가한 후 명령어를 실행합니다.
# openssl.cnf 파일을 찾거나 다운로드합니다. 보통 OpenSSL이 설치된 폴더 내에 openssl.cnf 파일이 위치해 있습니다.
# 예: C:\Program Files\OpenSSL-Win64\bin\openssl.cnf
# openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -config "C:\Program Files\OpenSSL-Win64\bin\openssl.cnf"
# openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -config "c:\devs\anaconda3\envs\py38_64_flask\Library\ssl\openssl.cnf"

# Country Name (2 letter code) [AU]: KR
# State or Province Name (full name) [Some-State]: Seoul
# Locality Name (eg, city) []: Seoul
# Organization Name (eg, company) [Internet Widgits Pty Ltd]: My Company
# Organizational Unit Name (eg, section) []: Development
# Common Name (e.g. server FQDN or YOUR name) []: localhost
# Email Address []: admin@example.com


from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, HTTPS!"

if __name__ == "__main__":
    # HTTPS 설정: SSL 인증서와 키 파일 지정
    app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=443)


