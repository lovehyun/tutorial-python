# 퀴즈 응시 시스템 완성

## 1. templates/quiz/quiz_take.html

```html
<!-- templates/quiz/quiz_take.html -->
{% extends 'base/base.html' %}

{% block title %}퀴즈 응시 - {{ quiz.title }}{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-9">
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h4>{{ quiz.title }}</h4>
                <div>
                    <span class="badge bg-primary">{{ answered_count }}/{{ total_questions }}</span>
                    <span id="timer" class="badge bg-info ms-2">00:00:00</span>
                </div>
            </div>
            <div class="card-body">
                <!-- 진행률 바 -->
                <div class="progress mb-4">
                    <div class="progress-bar" role="progressbar" 
                         style="width: {{ answered_count|floatformat:0 }}{{ total_questions|floatformat:0 }}%"
                         id="progress-bar">
                        {{ answered_count }}/{{ total_questions }}
                    </div>
                </div>

                <!-- 문제 목록 -->
                {% for question in questions %}
                <div class="question-container mb-4 p-4 border rounded" 
                     id="question-{{ question.id }}"
                     data-question-id="{{ question.id }}">
                    
                    <h5 class="question-title">
                        문제 {{ forloop.counter }}
                        {% if question.id in answered_questions %}
                            <span class="badge bg-success ms-2">완료</span>
                        {% endif %}
                    </h5>
                    
                    <p class="question-text">{{ question.question_text }}</p>
                    
                    {% if question.question_image %}
                        <img src="{{ question.question_image.url }}" 
                             class="img-fluid mb-3 question-image" 
                             alt="문제 이미지">
                    {% endif %}
                    
                    <!-- 선택지 -->
                    <div class="choices-container">
                        {% for choice in question.choices.all %}
                        <div class="choice-item mb-2">
                            <div class="form-check">
                                <input class="form-check-input choice-radio" 
                                       type="radio" 
                                       name="question_{{ question.id }}" 
                                       id="choice_{{ choice.id }}"
                                       value="{{ choice.id }}"
                                       data-question-id="{{ question.id }}"
                                       data-choice-id="{{ choice.id }}">
                                <label class="form-check-label choice-label" 
                                       for="choice_{{ choice.id }}">
                                    <span class="choice-number">{{ forloop.counter }}.</span>
                                    <span class="choice-text">{{ choice.choice_text }}</span>
                                </label>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    
                    <!-- 답안 제출 결과 표시 영역 -->
                    <div class="answer-result mt-3" id="result-{{ question.id }}" style="display: none;">
                        <div class="alert" id="alert-{{ question.id }}">
                            <div class="result-content"></div>
                        </div>
                    </div>
                </div>
                {% endfor %}

                <!-- 퀴즈 완료 버튼 -->
                <div class="text-center mt-4">
                    <button id="complete-quiz-btn" class="btn btn-success btn-lg" disabled>
                        퀴즈 완료하기
                    </button>
                    <div class="mt-2">
                        <small class="text-muted">모든 문제를 완료해야 퀴즈를 완료할 수 있습니다.</small>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- 사이드바 -->
    <div class="col-md-3">
        <div class="card sticky-top">
            <div class="card-header">
                <h6>문제 네비게이션</h6>
            </div>
            <div class="card-body">
                <div class="question-nav">
                    {% for question in questions %}
                    <button class="btn btn-outline-secondary btn-sm me-1 mb-1 question-nav-btn"
                            data-question-id="{{ question.id }}"
                            id="nav-btn-{{ question.id }}">
                        {{ forloop.counter }}
                    </button>
                    {% endfor %}
                </div>
                
                <hr>
                
                <div class="quiz-stats">
                    <p><strong>총 문제:</strong> {{ total_questions }}개</p>
                    <p><strong>완료:</strong> <span id="completed-count">{{ answered_count }}</span>개</p>
                    <p><strong>남은 문제:</strong> <span id="remaining-count">{{ total_questions|add:"-"|add:answered_count }}</span>개</p>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- JavaScript -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    const quizId = {{ quiz.id }};
    const totalQuestions = {{ total_questions }};
    let completedCount = {{ answered_count }};
    let startTime = new Date();
    
    // 타이머 시작
    updateTimer();
    setInterval(updateTimer, 1000);
    
    // 선택지 클릭 이벤트
    document.querySelectorAll('.choice-radio').forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.checked) {
                submitAnswer(this.dataset.questionId, this.dataset.choiceId);
            }
        });
    });
    
    // 문제 네비게이션 버튼 클릭
    document.querySelectorAll('.question-nav-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const questionId = this.dataset.questionId;
            const questionElement = document.getElementById('question-' + questionId);
            questionElement.scrollIntoView({ behavior: 'smooth' });
        });
    });
    
    // 퀴즈 완료 버튼 클릭
    document.getElementById('complete-quiz-btn').addEventListener('click', function() {
        if (completedCount === totalQuestions) {
            if (confirm('퀴즈를 완료하시겠습니까?')) {
                window.location.href = `/quiz/${quizId}/complete/`;
            }
        }
    });
    
    // 답안 제출 함수
    function submitAnswer(questionId, choiceId) {
        fetch(`/quiz/${quizId}/submit/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                question_id: questionId,
                choice_id: choiceId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAnswerResult(questionId, data);
                updateProgress(questionId);
            } else {
                alert('답안 제출 중 오류가 발생했습니다: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('네트워크 오류가 발생했습니다.');
        });
    }
    
    // 답안 결과 표시
    function showAnswerResult(questionId, data) {
        const resultDiv = document.getElementById('result-' + questionId);
        const alertDiv = document.getElementById('alert-' + questionId);
        const resultContent = alertDiv.querySelector('.result-content');
        
        if (data.is_correct) {
            alertDiv.className = 'alert alert-success';
            resultContent.innerHTML = '<strong>정답입니다!</strong>';
        } else {
            alertDiv.className = 'alert alert-danger';
            resultContent.innerHTML = '<strong>틀렸습니다.</strong>';
            
            // 정답 표시
            if (data.correct_choice_id) {
                const correctChoice = document.getElementById('choice_' + data.correct_choice_id);
                if (correctChoice) {
                    correctChoice.parentElement.parentElement.style.backgroundColor = '#d4edda';
                    correctChoice.parentElement.parentElement.style.border = '2px solid #28a745';
                }
            }
        }
        
        // 해설 표시
        if (data.explanation) {
            resultContent.innerHTML += '<br><strong>해설:</strong> ' + data.explanation;
        }
        
        resultDiv.style.display = 'block';
        
        // 선택지 비활성화
        const radios = document.querySelectorAll(`input[name="question_${questionId}"]`);
        radios.forEach(radio => radio.disabled = true);
    }
    
    // 진행률 업데이트
    function updateProgress(questionId) {
        // 네비게이션 버튼 업데이트
        const navBtn = document.getElementById('nav-btn-' + questionId);
        navBtn.classList.remove('btn-outline-secondary');
        navBtn.classList.add('btn-success');
        
        // 완료 배지 추가
        const questionTitle = document.querySelector('#question-' + questionId + ' .question-title');
        if (!questionTitle.querySelector('.badge')) {
            const badge = document.createElement('span');
            badge.className = 'badge bg-success ms-2';
            badge.textContent = '완료';
            questionTitle.appendChild(badge);
        }
        
        // 통계 업데이트
        completedCount++;
        document.getElementById('completed-count').textContent = completedCount;
        document.getElementById('remaining-count').textContent = totalQuestions - completedCount;
        
        // 진행률 바 업데이트
        const progressBar = document.getElementById('progress-bar');
        const percentage = (completedCount / totalQuestions) * 100;
        progressBar.style.width = percentage + '%';
        progressBar.textContent = completedCount + '/' + totalQuestions;
        
        // 완료 버튼 활성화
        if (completedCount === totalQuestions) {
            document.getElementById('complete-quiz-btn').disabled = false;
        }
    }
    
    // 타이머 업데이트
    function updateTimer() {
        const now = new Date();
        const elapsed = Math.floor((now - startTime) / 1000);
        const hours = Math.floor(elapsed / 3600);
        const minutes = Math.floor((elapsed % 3600) / 60);
        const seconds = elapsed % 60;
        
        const timeString = String(hours).padStart(2, '0') + ':' + 
                          String(minutes).padStart(2, '0') + ':' + 
                          String(seconds).padStart(2, '0');
        
        document.getElementById('timer').textContent = timeString;
    }
    
    // CSRF 토큰 가져오기
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
</script>

<style>
.question-container {
    transition: all 0.3s ease;
}

.question-container:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.choice-item {
    transition: all 0.2s ease;
}

.choice-item:hover {
    background-color: #f8f9fa;
    border-radius: 5px;
    padding: 5px;
}

.choice-label {
    cursor: pointer;
    width: 100%;
    margin-bottom: 0;
}

.choice-number {
    font-weight: bold;
    margin-right: 8px;
}

.question-nav-btn {
    width: 40px;
    height: 40px;
}

.quiz-stats p {
    margin-bottom: 0.5rem;
}

.sticky-top {
    top: 20px;
}

@media (max-width: 768px) {
    .question-nav-btn {
        width: 35px;
        height: 35px;
        font-size: 0.8rem;
    }
}
</style>
{% endblock %}
```

## 2. templates/quiz/quiz_complete.html

```html
<!-- templates/quiz/quiz_complete.html -->
{% extends 'base/base.html' %}

{% block title %}퀴즈 완료 - {{ quiz.title }}{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <!-- 결과 요약 -->
        <div class="card mb-4">
            <div class="card-header text-center bg-primary text-white">
                <h3>퀴즈 완료!</h3>
            </div>
            <div class="card-body text-center">
                <div class="row">
                    <div class="col-md-3">
                        <div class="score-display">
                            <h2 class="display-4 text-primary">{{ percentage }}%</h2>
                            <p class="text-muted">총점</p>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="score-detail">
                            <h4 class="text-success">{{ correct_count }}</h4>
                            <p class="text-muted">정답</p>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="score-detail">
                            <h4 class="text-danger">{{ wrong_count }}</h4>
                            <p class="text-muted">오답</p>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="score-detail">
                            <h4 class="text-info">{{ quiz.total_questions }}</h4>
                            <p class="text-muted">총 문제</p>
                        </div>
                    </div>
                </div>
                
                {% if quiz.time_taken %}
                <div class="mt-3">
                    <p><strong>소요 시간:</strong> 
                        {% if quiz.time_taken.seconds >= 3600 %}
                            {{ quiz.time_taken.seconds|floatformat:0|div:3600 }}시간 
                        {% endif %}
                        {{ quiz.time_taken.seconds|floatformat:0|mod:3600|div:60 }}분 
                        {{ quiz.time_taken.seconds|mod:60 }}초
                    </p>
                </div>
                {% endif %}
                
                <!-- 성과 메시지 -->
                <div class="achievement mt-3">
                    {% if percentage >= 90 %}
                        <div class="alert alert-success">
                            <h5>🎉 우수한 성과입니다!</h5>
                            <p>90점 이상의 훌륭한 점수를 받으셨습니다!</p>
                        </div>
                    {% elif percentage >= 70 %}
                        <div class="alert alert-info">
                            <h5>👍 좋은 성과입니다!</h5>
                            <p>70점 이상의 좋은 점수입니다. 조금 더 공부하면 더 좋은 결과를 얻을 수 있을 것 같아요!</p>
                        </div>
                    {% elif percentage >= 50 %}
                        <div class="alert alert-warning">
                            <h5>📚 더 열심히 공부해보세요!</h5>
                            <p>기본기는 갖추었지만 더 많은 연습이 필요합니다.</p>
                        </div>
                    {% else %}
                        <div class="alert alert-danger">
                            <h5>💪 다시 도전해보세요!</h5>
                            <p>조금 더 공부한 후 다시 시도해보시기 바랍니다.</p>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>

        <!-- 상세 결과 -->
        <div class="card">
            <div class="card-header">
                <h5>상세 결과</h5>
            </div>
            <div class="card-body">
                {% for result in results %}
                <div class="result-item mb-4 p-3 border rounded">
                    <div class="d-flex justify-content-between align-items-start">
                        <h6>문제 {{ forloop.counter }}</h6>
                        {% if result.is_correct %}
                            <span class="badge bg-success">정답</span>
                        {% else %}
                            <span class="badge bg-danger">오답</span>
                        {% endif %}
                    </div>
                    
                    <p class="question-text mt-2">{{ result.question.question_text }}</p>
                    
                    <div class="choices-review">
                        {% for choice in result.question.choices.all %}
                        <div class="choice-review mb-1 p-2 rounded
                                    {% if choice.is_correct %}bg-success text-white
                                    {% elif choice == result.selected_choice and not choice.is_correct %}bg-danger text-white
                                    {% elif choice == result.selected_choice %}bg-primary text-white
                                    {% else %}bg-light{% endif %}">
                            <span class="fw-bold">{{ forloop.counter }}.</span> {{ choice.choice_text }}
                            {% if choice.is_correct %}
                                <span class="badge bg-warning text-dark ms-2">정답</span>
                            {% endif %}
                            {% if choice == result.selected_choice %}
                                <span class="badge bg-info ms-2">선택</span>
                            {% endif %}
                        </div>
                        {% endfor %}
                    </div>
                    
                    {% if result.question.explanation %}
                    <div class="explanation mt-3">
                        <strong>해설:</strong> {{ result.question.explanation }}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- 액션 버튼들 -->
        <div class="text-center mt-4 mb-4">
            <a href="{% url 'quiz:question_set_detail' quiz.question_set.pk %}" class="btn btn-primary">
                문제집으로 돌아가기
            </a>
            <a href="{% url 'quiz:quiz_start' quiz.question_set.pk %}" class="btn btn-success">
                다시 도전하기
            </a>
            <a href="{% url 'quiz:my_quizzes' %}" class="btn btn-info">
                내 퀴즈 기록 보기
            </a>
            <a href="{% url 'quiz:question_list' %}" class="btn btn-secondary">
                다른 문제집 보기
            </a>
        </div>
    </div>
</div>

<style>
.score-display .display-4 {
    font-weight: bold;
}

.score-detail h4 {
    font-weight: bold;
    margin-bottom: 0;
}

.result-item {
    border-left: 4px solid #007bff;
}

.choice-review {
    transition: all 0.2s ease;
}

.achievement {
    border-radius: 10px;
}

@media (max-width: 768px) {
    .score-display .display-4 {
        font-size: 2.5rem;
    }
    
    .score-detail h4 {
        font-size: 1.5rem;
    }
}
</style>
{% endblock %}
```

## 3. templates/quiz/my_quizzes.html

```html
<!-- templates/quiz/my_quizzes.html -->
{% extends 'base/base.html' %}

{% block title %}내 퀴즈 기록 - Quizlet 클론{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>내 퀴즈 기록</h2>
</div>

{% if quizzes %}
<div class="row">
    {% for quiz in quizzes %}
    <div class="col-md-6 mb-3">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">{{ quiz.question_set.title }}</h5>
                <p class="card-text">{{ quiz.question_set.description|truncatewords:15 }}</p>
                
                <div class="quiz-stats">
                    <div class="row text-center">
                        <div class="col-3">
                            <strong class="text-primary">{{ quiz.get_percentage_score }}%</strong>
                            <br><small class="text-muted">점수</small>
                        </div>
                        <div class="col-3">
                            <strong class="text-success">{{ quiz.score }}</strong>
                            <br><small class="text-muted">정답</small>
                        </div>
                        <div class="col-3">
                            <strong class="text-info">{{ quiz.total_questions }}</strong>
                            <br><small class="text-muted">총 문제</small>
                        </div>
                        <div class="col-3">
                            {% if quiz.time_taken %}
                            <strong class="text-warning">{{ quiz.time_taken.seconds|floatformat:0|div:60 }}분</strong>
                            <br><small class="text-muted">소요 시간</small>
                            {% else %}
                            <strong class="text-muted">-</strong>
                            <br><small class="text-muted">시간</small>
                            {% endif %}
                        </div>
                    </div>
                </div>
                
                <hr>
                
                <div class="d-flex justify-content-between align-items-center">
                    <small class="text-muted">
                        {% if quiz.is_completed %}
                            {{ quiz.completed_at|date:"m월 d일 H:i" }} 완료
                        {% else %}
                            {{ quiz.started_at|date:"m월 d일 H:i" }} 시작 (미완료)
                        {% endif %}
                    </small>
                    
                    <div>
                        {% if quiz.is_completed %}
                            <a href="{% url 'quiz:quiz_complete' quiz.id %}" class="btn btn-sm btn-primary">
                                결과 보기
                            </a>
                        {% else %}
                            <a href="{% url 'quiz:quiz_take' quiz.id %}" class="btn btn-sm btn-warning">
                                계속하기
                            </a>
                        {% endif %}
                        <a href="{% url 'quiz:quiz_start' quiz.question_set.pk %}" class="btn btn-sm btn-success">
                            다시 도전
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% endfor %}
</div>

<!-- 페이지네이션 (나중에 추가 가능) -->
{% else %}
<div class="text-center">
    <div class="alert alert-info">
        <h4>아직 퀴즈 기록이 없습니다</h4>
        <p>문제집에서 퀴즈를 시작해보세요!</p>
        <a href="{% url 'quiz:question_list' %}" class="btn btn-primary">문제집 보러가기</a>
    </div>
</div>
{% endif %}
{% endblock %}
```

## 4. 네비게이션 바에 "내 퀴즈 기록" 링크 추가

base.html의 네비게이션 부분을 수정:

```html
<!-- templates/base/base.html 의 네비게이션 부분 -->
<ul class="navbar-nav me-auto">
    <li class="nav-item">
        <a class="nav-link" href="{% url 'quiz:home' %}">홈</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="{% url 'quiz:question_list' %}">문제집 목록</a>
    </li>
    {% if user.is_authenticated %}
    <li class="nav-item">
        <a class="nav-link" href="{% url 'quiz:my_quizzes' %}">내 퀴즈 기록</a>
    </li>
    {% endif %}
</ul>
```

## 5. 테스트해보기

1. **퀴즈 시작**: 문제집 상세 페이지에서 "퀴즈 시작" 클릭
2. **문제 풀기**: 선택지 클릭하면 실시간으로 정답/오답 표시
3. **진행률 확인**: 상단 진행률 바와 사이드바 네비게이션
4. **퀴즈 완료**: 모든 문제 완료 후 결과 페이지
5. **기록 확인**: "내 퀴즈 기록"에서 과거 퀴즈 확인

이제 완전한 퀴즈 시스템이 완성되었습니다! 🎉
