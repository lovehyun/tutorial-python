# routes/result_routes.py
# 시험 결과 저장 및 통계 관련 라우트

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_required, current_user
import json
from datetime import datetime, timedelta
import sqlite3
from database import get_db_connection, get_quiz_session, deactivate_quiz_session

result_bp = Blueprint('result', __name__)

@result_bp.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    """시험 제출 및 채점"""
    session_token = request.form.get('session_token')
    if not session_token:
        flash('시험 세션이 유효하지 않습니다. 다시 시작해주세요.', 'error')
        return redirect(url_for('quiz.dashboard'))
    
    # 데이터베이스에서 퀴즈 세션 조회
    quiz_session = get_quiz_session(session_token)
    if not quiz_session or quiz_session['user_id'] != current_user.id:
        flash('시험 세션이 만료되었거나 유효하지 않습니다. 다시 시작해주세요.', 'error')
        return redirect(url_for('quiz.dashboard'))
    
    questions = quiz_session['questions_data']
    file_id = quiz_session['quiz_file_id']
    settings = quiz_session['settings']
    
    results = []
    answers_payload = {}
    correct_count = 0
    
    # 각 문제 채점
    for display_id, question in questions.items():
        user_display_answer = request.form.get(f'question_{display_id}')
        is_correct = False
        user_real_answer = None
        
        if user_display_answer:
            user_display_answer = int(user_display_answer)
            # 표시된 선택지 번호를 원래 번호로 변환
            display_to_original = {
                item['display_index']: item['original_index']
                for item in question['shuffled_choices']
            }
            user_real_answer = display_to_original.get(user_display_answer)
            is_correct = user_real_answer == question['answer']
            if is_correct:
                correct_count += 1
        
        results.append({
            'question': question,
            'user_answer': user_display_answer,
            'real_answer': user_real_answer,
            'is_correct': is_correct
        })
        answers_payload[str(display_id)] = {
            'question': question['question'],
            'user_display_answer': user_display_answer,
            'user_real_answer': user_real_answer,
            'correct_answer': question['answer'],
            'choices': question['shuffled_choices']
        }
    
    total_questions = len(questions)
    score_percentage = round((correct_count / total_questions) * 100, 1)
    
    # 결과를 데이터베이스에 저장
    conn = get_db_connection()
    import json as _json
    conn.execute('''
        INSERT INTO quiz_results 
        (user_id, quiz_file_id, score, total_questions, correct_answers, settings, answers)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        current_user.id,
        file_id,
        score_percentage,
        total_questions,
        correct_count,
        json.dumps(settings),
        _json.dumps(answers_payload)
    ))
    conn.commit()
    conn.close()
    
    # 퀴즈 세션 비활성화
    deactivate_quiz_session(session_token)
    
    return render_template('result/result.html', 
                         results=results, 
                         correct_count=correct_count,
                         total_questions=total_questions, 
                         score_percentage=score_percentage)

@result_bp.route('/stats', defaults={'period': 'recent10'})
@result_bp.route('/stats/<period>')
@login_required
def stats(period):
    """통계 대시보드"""
    conn = get_db_connection()
    
    # 기간별 쿼리 조건 설정
    if period == 'recent10':
        query = '''
            SELECT qr.score, qr.created_at, qf.original_filename
            FROM quiz_results qr
            JOIN quiz_files qf ON qr.quiz_file_id = qf.id
            WHERE qr.user_id = ?
            ORDER BY qr.created_at DESC
            LIMIT 10
        '''
        params = (current_user.id,)
    elif period == 'recent30':
        query = '''
            SELECT qr.score, qr.created_at, qf.original_filename
            FROM quiz_results qr
            JOIN quiz_files qf ON qr.quiz_file_id = qf.id
            WHERE qr.user_id = ?
            ORDER BY qr.created_at DESC
            LIMIT 30
        '''
        params = (current_user.id,)
    elif period == 'last30days':
        thirty_days_ago = datetime.now() - timedelta(days=30)
        query = '''
            SELECT qr.score, qr.created_at, qf.original_filename
            FROM quiz_results qr
            JOIN quiz_files qf ON qr.quiz_file_id = qf.id
            WHERE qr.user_id = ? AND qr.created_at >= ?
            ORDER BY qr.created_at DESC
        '''
        params = (current_user.id, thirty_days_ago)
    else:  # 'all'
        query = '''
            SELECT qr.score, qr.created_at, qf.original_filename
            FROM quiz_results qr
            JOIN quiz_files qf ON qr.quiz_file_id = qf.id
            WHERE qr.user_id = ?
            ORDER BY qr.created_at DESC
        '''
        params = (current_user.id,)
    
    results = conn.execute(query, params).fetchall()
    conn.close()
    
    # 데이터 포맷팅
    data = []
    for result in reversed(results):  # 시간순으로 정렬
        data.append({
            'x': result['created_at'][:16],  # 'YYYY-MM-DD HH:MM' 형식
            'y': result['score'],
            'date': result['created_at'],
            'filename': result['original_filename']
        })
    
    # 통계 계산
    scores = [r['score'] for r in results]
    stats_summary = {
        'count': len(scores),
        'average': round(sum(scores) / len(scores), 1) if scores else 0,
        'max': max(scores) if scores else 0,
        'min': min(scores) if scores else 0
    }
    
    return render_template(
        'result/stats.html',
        data=data,
        stats=stats_summary,
        period=period
    )

@result_bp.route('/history')
@login_required
def history():
    """시험 히스토리 페이지"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    
    conn = get_db_connection()
    
    # 총 결과 수
    total_count = conn.execute(
        'SELECT COUNT(*) as count FROM quiz_results WHERE user_id = ?',
        (current_user.id,)
    ).fetchone()['count']
    
    # 페이지별 결과
    results = conn.execute('''
        SELECT qr.*, qf.original_filename
        FROM quiz_results qr
        JOIN quiz_files qf ON qr.quiz_file_id = qf.id
        WHERE qr.user_id = ?
        ORDER BY qr.created_at DESC
        LIMIT ? OFFSET ?
    ''', (current_user.id, per_page, offset)).fetchall()
    
    conn.close()
    
    # 페이지네이션 정보
    has_prev = page > 1
    has_next = offset + per_page < total_count
    total_pages = (total_count + per_page - 1) // per_page
    
    return render_template('result/history.html',
                         results=results,
                         page=page,
                         has_prev=has_prev,
                         has_next=has_next,
                         total_pages=total_pages,
                         total_count=total_count)

@result_bp.route('/detail/<int:result_id>')
@login_required
def detail(result_id):
    """특정 시험 결과 상세보기"""
    conn = get_db_connection()
    
    # 결과 정보 (소유권 확인 포함)
    if getattr(current_user, 'is_admin', False):
        # 관리자는 모든 결과 열람 가능
        result = conn.execute('''
            SELECT qr.*, qf.original_filename, qf.file_path, u.username AS user_username, u.email AS user_email
            FROM quiz_results qr
            JOIN quiz_files qf ON qr.quiz_file_id = qf.id
            JOIN users u ON u.id = qr.user_id
            WHERE qr.id = ?
        ''', (result_id,)).fetchone()
    else:
        result = conn.execute('''
            SELECT qr.*, qf.original_filename, qf.file_path, u.username AS user_username, u.email AS user_email
            FROM quiz_results qr
            JOIN quiz_files qf ON qr.quiz_file_id = qf.id
            JOIN users u ON u.id = qr.user_id
            WHERE qr.id = ? AND qr.user_id = ?
        ''', (result_id, current_user.id)).fetchone()
    
    conn.close()
    
    if not result:
        flash('결과를 찾을 수 없습니다.', 'error')
        return redirect(url_for('result.history'))
    
    # 설정 정보 파싱
    settings = {}
    if result and ('settings' in result.keys()) and result['settings']:
        settings = json.loads(result['settings'])
    answers = {}
    try:
        if result and 'answers' in result.keys() and result['answers']:
            answers = json.loads(result['answers'])
    except Exception:
        answers = {}
    
    return render_template('result/result_detail.html', result=result, settings=settings, answers=answers)

@result_bp.route('/delete/<int:result_id>', methods=['POST'])
@login_required
def delete_result(result_id):
    """시험 결과 삭제"""
    conn = get_db_connection()
    
    # 소유권 확인 후 삭제
    result = conn.execute(
        'SELECT id FROM quiz_results WHERE id = ? AND user_id = ?',
        (result_id, current_user.id)
    ).fetchone()
    
    if result:
        conn.execute('DELETE FROM quiz_results WHERE id = ?', (result_id,))
        conn.commit()
        flash('시험 결과가 삭제되었습니다.', 'success')
    else:
        flash('삭제할 수 없습니다.', 'error')
    
    conn.close()
    return redirect(url_for('result.history'))
