# streamlit 설치
pip install streamlit

# streamlit 설치 버전 확인
streamlit --version

# 기본 데모
streamlit hello
python -m streamlit hello

# 메뉴얼
streamlit docs

# 실행
streamlit run app.py
python -m streamlit run app.py

# 설정
## 설정파일
.streamlit/config.toml:
[server]
port = 80

## 설정파일 위치 (윈도우 기준)
C:/Users/.../.streamlit/config.toml

## 각종 환경변수
export STREAMLIT_SERVER_PORT=80

## 실행 (옵션)
streamlit run --help

streamlit run <script.py> --server.port 80
