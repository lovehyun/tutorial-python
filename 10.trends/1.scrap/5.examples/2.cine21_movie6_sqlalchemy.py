from flask import Flask, redirect, url_for, render_template, request, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    audience = db.Column(db.String(100), nullable=False)

    def __init__(self, rank, title, audience):
        self.rank = rank
        self.title = title
        self.audience = audience

def save_to_db(rank, title, audience):
    movie = Movie(rank=rank, title=title, audience=audience)
    db.session.add(movie)
    db.session.commit()

def get_movie_lists(driver):
    boxoffice_list_content = driver.find_element(By.CSS_SELECTOR, 'div#boxoffice_list_content')
    boxoffice_li_list = boxoffice_list_content.find_elements(By.CSS_SELECTOR, 'li.boxoffice_li')

    for _, boxoffice_li in enumerate(boxoffice_li_list, start=1):
        rank_span = boxoffice_li.find_element(By.CSS_SELECTOR, 'span.grade')
        mov_name_div = boxoffice_li.find_element(By.CSS_SELECTOR, 'div.mov_name')
        people_num_div = boxoffice_li.find_element(By.CSS_SELECTOR, 'div.people_num')

        rank = rank_span.text.strip()
        mov_name = mov_name_div.text.strip() if mov_name_div else ''
        people_num = people_num_div.text.strip() if people_num_div else ''
        
        print(f"순위: {rank}, 영화 제목: {mov_name}, 관객 수: {people_num}")
        save_to_db(rank, mov_name, people_num)

def scrape_and_save_movies():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    url = 'http://www.cine21.com/rank/boxoffice/domestic'
    driver.get(url)
    driver.implicitly_wait(2)
    wait = WebDriverWait(driver, 10)

    get_movie_lists(driver)

    for page in range(2, 11):
        page_a_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.page a")))
        if page <= len(page_a_tags):
            page_a_tags[page - 1].click()
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#boxoffice_list_content li.boxoffice_li')))
            time.sleep(2)
            get_movie_lists(driver)
    driver.quit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form["action"]
        if action == "scrape":
            scrape_and_save_movies()
            flash("Data scraped and saved successfully!")
        elif action == "view":
            movies = Movie.query.all()
            return render_template("index.html", movies=movies, view=True)
        elif action == "clear":
            db.session.query(Movie).delete()
            db.session.commit()
            flash("Database cleared successfully!")
        return redirect(url_for("index"))

    return render_template("index.html", movies=None, view=False)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
