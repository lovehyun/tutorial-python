# pip install flask python-dotenv openai
import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

# static_url_path=''는 정적 파일의 URL 경로 접두사를 설정합니다.
#  - static_url_path='': /styles.css로 접근 가능
#  - 설정 없을 때: /static/styles.css로 접근해야 함
app = Flask(__name__, static_folder='public', static_url_path='')
openai = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# In-memory storage for reviews
reviews = []

@app.route('/api/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    rating = data.get('rating')
    opinion = data.get('opinion')

    if not rating or not opinion:
        return jsonify({'error': 'Rating and opinion are required'}), 400

    reviews.append({'rating': rating, 'opinion': opinion})
    return jsonify({'message': 'Review added successfully'}), 201

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    return jsonify({'reviews': reviews})

@app.route('/api/ai-summary', methods=['GET'])
def get_ai_summary():
    if not reviews:
        return jsonify({'summary': '리뷰가 없습니다.', 'averageRating': 0})

    average_rating = sum(review['rating'] for review in reviews) / len(reviews)
    reviews_text = '\n'.join([f"별점: {review['rating']}, 내용: {review['opinion']}" 
                             for review in reviews])

    try:
        response = openai.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{
                'role': 'user',
                'content': f'다음 리뷰 목록을 기반으로 간결한 한글 요약을 작성하세요:\n\n{reviews_text}'
            }]
        )
        summary = response.choices[0].message.content.strip()
        return jsonify({'summary': summary, 'averageRating': average_rating})
    except Exception as e:
        app.logger.error(f'Error generating AI summary: {str(e)}')
        return jsonify({'error': 'Failed to generate AI summary'}), 500

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
