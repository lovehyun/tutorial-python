# pip install flask flask-sqlalchemy flask-socketio selenium webdriver-manager

from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading

# Flask 애플리케이션 설정
app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy와 SocketIO 초기화
db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode='threading')

scraping_thread = None
stop_scraping = False

# 영화 데이터를 저장할 Movie 모델 정의
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    audience = db.Column(db.String(100), nullable=False)

    def __init__(self, rank, title, audience):
        self.rank = rank
        self.title = title
        self.audience = audience

# 영화 데이터를 데이터베이스에 저장하는 함수
def save_to_db(rank, title, audience):
    movie = Movie(rank=rank, title=title, audience=audience)
    db.session.add(movie)
    db.session.commit()

# 영화 목록을 가져오는 함수
def get_movie_lists(driver):
    global stop_scraping

    boxoffice_list_content = driver.find_element(By.CSS_SELECTOR, 'div#boxoffice_list_content')
    boxoffice_li_list = boxoffice_list_content.find_elements(By.CSS_SELECTOR, 'li.boxoffice_li')

    for _, boxoffice_li in enumerate(boxoffice_li_list, start=1):
        if stop_scraping:
            break

        rank_span = boxoffice_li.find_element(By.CSS_SELECTOR, 'span.grade')
        mov_name_div = boxoffice_li.find_element(By.CSS_SELECTOR, 'div.mov_name')
        people_num_div = boxoffice_li.find_element(By.CSS_SELECTOR, 'div.people_num')

        rank = rank_span.text.strip()
        mov_name = mov_name_div.text.strip() if mov_name_div else ''
        people_num = people_num_div.text.strip() if people_num_div else ''
        
        print(f"순위: {rank}, 영화 제목: {mov_name}, 관객 수: {people_num}")
        socketio.emit('movie_data', {'rank': rank, 'mov_name': mov_name, 'people_num': people_num}, namespace='/')
        save_to_db(rank, mov_name, people_num)

# 영화를 스크래핑하고 저장하는 함수
def scrape_and_save_movies():
    global stop_scraping
    stop_scraping = False

    with app.app_context():  # 애플리케이션 컨텍스트 설정
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        url = 'http://www.cine21.com/rank/boxoffice/domestic'
        driver.get(url)
        driver.implicitly_wait(2)
        wait = WebDriverWait(driver, 10)

        total_pages = 10
        for page in range(1, total_pages + 1):
            if stop_scraping:
                break
    
            get_movie_lists(driver)
            socketio.emit('progress', {'page': page, 'total_pages': total_pages}, namespace='/')
            socketio.sleep(0.1)  # 조금 대기하여 이벤트가 프런트엔드로 전달되도록 함
            print(f"Page {page}/{total_pages} scraped")

            if page < total_pages:
                page_a_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.page a")))
                page_a_tags[page - 1].click()
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#boxoffice_list_content li.boxoffice_li')))
                time.sleep(2)
        driver.quit()
        socketio.emit('progress', {'page': total_pages, 'total_pages': total_pages, 'completed': True}, namespace='/')

# 루트 라우트 정의
@app.route("/", methods=["GET", "POST"])
def index():
    global scraping_thread, stop_scraping

    if request.method == "POST":
        action = request.form["action"]
        if action == "scrape":
            if scraping_thread and scraping_thread.is_alive():
                stop_scraping = True
                scraping_thread.join()
                scraping_thread = None
                flash("Scraping stopped.")
            else:
                scraping_thread = threading.Thread(target=scrape_and_save_movies)
                scraping_thread.start()
                flash("Scraping started! Check the progress below.")
        elif action == "view":
            movies = Movie.query.all()
            return render_template("index2.html", movies=movies, view=True, scraping_thread=scraping_thread)
        elif action == "clear":
            db.session.query(Movie).delete()
            db.session.commit()
            flash("Database cleared successfully!")
        return redirect(url_for("index"))
    
    return render_template("index2.html", movies=None, view=False, scraping_thread=scraping_thread)

# 클라이언트가 연결되었을 때 실행
@socketio.on('connect')
def handle_connect():
    print("Client connected")

# 클라이언트가 연결을 끊었을 때 실행
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

# 애플리케이션 실행
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True, port=5000)
