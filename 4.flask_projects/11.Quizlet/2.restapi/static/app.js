class QuizApp {
    constructor() {
        this.questions = [];
        this.userAnswers = {};
        this.initEventListeners();
        this.checkStatus();
    }

    initEventListeners() {
        // 템플릿 다운로드
        document.getElementById('downloadBtn').addEventListener('click', () => {
            window.location.href = '/api/download-template';
        });

        // 파일 업로드
        document.getElementById('uploadBtn').addEventListener('click', () => {
            this.uploadFile();
        });

        // 공부 모드
        document.getElementById('studyBtn').addEventListener('click', () => {
            this.loadStudyMode();
        });

        // 시험 모드
        document.getElementById('quizBtn').addEventListener('click', () => {
            this.loadQuizMode();
        });
    }

    showAlert(message, type = 'info') {
        const alertContainer = document.getElementById('alert-container');
        alertContainer.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // 3초 후 자동 제거
        setTimeout(() => {
            const alert = alertContainer.querySelector('.alert');
            if (alert) {
                alert.remove();
            }
        }, 3000);
    }

    async uploadFile() {
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];

        if (!file) {
            this.showAlert('파일을 선택해주세요.', 'warning');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                this.showAlert(data.message, 'success');
                this.updateQuizSection(data.question_count);
            } else {
                this.showAlert(data.error, 'danger');
            }
        } catch (error) {
            this.showAlert('업로드 중 오류가 발생했습니다.', 'danger');
        }
    }

    updateQuizSection(questionCount) {
        document.getElementById('question-info').textContent = `현재 문제: ${questionCount}개`;
        document.getElementById('quiz-section').style.display = 'block';
    }

    async checkStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();

            if (data.has_questions) {
                this.updateQuizSection(data.question_count);
            }
        } catch (error) {
            console.error('상태 확인 실패:', error);
        }
    }

    async loadStudyMode() {
        try {
            const response = await fetch('/api/questions');
            const data = await response.json();

            if (response.ok) {
                this.questions = data.questions;
                this.renderStudyMode();
            } else {
                this.showAlert(data.error, 'danger');
            }
        } catch (error) {
            this.showAlert('문제 로딩 중 오류가 발생했습니다.', 'danger');
        }
    }

    // HTML 태그를 안전하게 이스케이프하는 함수
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    renderStudyMode() {
        const container = document.getElementById('study-container');
        let html = `
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>공부 모드</h2>
                <button class="btn btn-secondary back-btn" onclick="app.goHome()">홈으로</button>
            </div>
        `;

        this.questions.forEach(question => {
            const choices = [question.choice1, question.choice2, question.choice3, question.choice4];
            
            html += `
                <div class="card mb-4 question-card">
                    <div class="card-header">
                        <h5>문제 ${question.id}</h5>
                    </div>
                    <div class="card-body">
                        <p class="card-text fs-5">${this.escapeHtml(question.question)}</p>
                        
                        <div class="row">
                            ${choices.map((choice, index) => `
                                <div class="col-md-6 mb-2">
                                    <div class="p-2 border rounded ${index + 1 === question.answer ? 'bg-success text-white' : 'bg-light'}">
                                        <strong>${index + 1}.</strong> ${this.escapeHtml(choice)}
                                        ${index + 1 === question.answer ? '<span class="badge bg-warning text-dark ms-2">정답</span>' : ''}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                        
                        ${question.explanation ? `
                            <div class="alert alert-info mt-3">
                                <strong>해설:</strong> ${this.escapeHtml(question.explanation)}
                            </div>
                        ` : ''}
                    </div>
                </div>
            `;
        });

        html += `
            <div class="text-center mb-4">
                <button class="btn btn-primary btn-lg" onclick="app.loadQuizMode()">시험 모드로 이동</button>
            </div>
        `;

        container.innerHTML = html;
        this.showContainer('study-container');
    }

    async loadQuizMode() {
        try {
            const response = await fetch('/api/quiz');
            const data = await response.json();

            if (response.ok) {
                this.questions = data.questions;
                this.userAnswers = {};
                this.renderQuizMode();
            } else {
                this.showAlert(data.error, 'danger');
            }
        } catch (error) {
            this.showAlert('퀴즈 로딩 중 오류가 발생했습니다.', 'danger');
        }
    }

    renderQuizMode() {
        const container = document.getElementById('quiz-container');
        let html = `
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>시험 모드</h2>
                <button class="btn btn-secondary back-btn" onclick="app.goHome()">홈으로</button>
            </div>
            
            <div class="alert alert-warning">
                <strong>주의:</strong> 모든 문제를 풀고 제출 버튼을 눌러야 채점됩니다.
            </div>
        `;

        this.questions.forEach(question => {
            const choices = [question.choice1, question.choice2, question.choice3, question.choice4];
            
            html += `
                <div class="card mb-4 question-card">
                    <div class="card-header">
                        <h5>문제 ${question.id}</h5>
                    </div>
                    <div class="card-body">
                        <p class="card-text fs-5">${this.escapeHtml(question.question)}</p>
                        
                        ${choices.map((choice, index) => `
                            <div class="form-check mb-2">
                                <input class="form-check-input" type="radio" 
                                       name="question_${question.id}" 
                                       id="q${question.id}_${index + 1}"
                                       value="${index + 1}"
                                       onchange="app.saveAnswer(${question.id}, ${index + 1})">
                                <label class="form-check-label" for="q${question.id}_${index + 1}">
                                    <strong>${index + 1}.</strong> ${this.escapeHtml(choice)}
                                </label>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        });

        html += `
            <div class="text-center mb-4">
                <button class="btn btn-success btn-lg" onclick="app.submitQuiz()">시험 제출하기</button>
            </div>
        `;

        container.innerHTML = html;
        this.showContainer('quiz-container');
    }

    saveAnswer(questionId, answer) {
        this.userAnswers[questionId] = answer;
    }

    async submitQuiz() {
        try {
            const response = await fetch('/api/submit-quiz', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    answers: this.userAnswers
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.renderResult(data);
            } else {
                this.showAlert(data.error, 'danger');
            }
        } catch (error) {
            this.showAlert('제출 중 오류가 발생했습니다.', 'danger');
        }
    }

    renderResult(data) {
        const container = document.getElementById('result-container');
        let html = `
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>시험 결과</h2>
                <button class="btn btn-secondary back-btn" onclick="app.goHome()">홈으로</button>
            </div>
            
            <!-- 결과 요약 -->
            <div class="card mb-4">
                <div class="card-header text-center bg-primary text-white">
                    <h3>채점 결과</h3>
                </div>
                <div class="card-body text-center">
                    <div class="row">
                        <div class="col-md-3">
                            <h2 class="text-primary">${data.score_percentage}%</h2>
                            <p>총점</p>
                        </div>
                        <div class="col-md-3">
                            <h3 class="text-success">${data.correct_count}</h3>
                            <p>정답</p>
                        </div>
                        <div class="col-md-3">
                            <h3 class="text-danger">${data.total_questions - data.correct_count}</h3>
                            <p>오답</p>
                        </div>
                        <div class="col-md-3">
                            <h3 class="text-info">${data.total_questions}</h3>
                            <p>총 문제</p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // 문제별 결과
        data.results.forEach(result => {
            const question = result.question;
            const choices = [question.choice1, question.choice2, question.choice3, question.choice4];
            
            html += `
                <div class="card mb-3">
                    <div class="card-header d-flex justify-content-between">
                        <h6>문제 ${question.id}</h6>
                        <span class="badge ${result.is_correct ? 'bg-success' : 'bg-danger'}">
                            ${result.is_correct ? '정답' : '오답'}
                        </span>
                    </div>
                    <div class="card-body">
                        <p class="fw-bold">${this.escapeHtml(question.question)}</p>
                        
                        ${choices.map((choice, index) => {
                            let cssClass = 'bg-light';
                            let badges = '';
                            
                            if (index + 1 === question.answer) {
                                cssClass = 'bg-success text-white';
                                badges += '<span class="badge bg-warning text-dark ms-2">정답</span>';
                            } else if (index + 1 === result.user_answer && !result.is_correct) {
                                cssClass = 'bg-danger text-white';
                            }
                            
                            if (index + 1 === result.user_answer) {
                                badges += '<span class="badge bg-info ms-2">선택</span>';
                            }
                            
                            return `
                                <div class="p-2 mb-1 rounded ${cssClass}">
                                    <strong>${index + 1}.</strong> ${this.escapeHtml(choice)} ${badges}
                                </div>
                            `;
                        }).join('')}
                        
                        ${question.explanation ? `
                            <div class="alert alert-info mt-3 mb-0">
                                <strong>해설:</strong> ${this.escapeHtml(question.explanation)}
                            </div>
                        ` : ''}
                    </div>
                </div>
            `;
        });

        html += `
            <div class="text-center mb-4">
                <button class="btn btn-info" onclick="app.loadStudyMode()">공부 모드로</button>
                <button class="btn btn-warning" onclick="app.loadQuizMode()">다시 시험보기</button>
            </div>
        `;

        container.innerHTML = html;
        this.showContainer('result-container');
    }

    showContainer(containerId) {
        // 모든 컨테이너 숨기기
        document.querySelector('.card').style.display = 'none';
        document.getElementById('study-container').style.display = 'none';
        document.getElementById('quiz-container').style.display = 'none';
        document.getElementById('result-container').style.display = 'none';
        
        // 선택된 컨테이너만 보이기
        document.getElementById(containerId).style.display = 'block';
    }

    goHome() {
        // 모든 컨테이너 숨기기
        document.getElementById('study-container').style.display = 'none';
        document.getElementById('quiz-container').style.display = 'none';
        document.getElementById('result-container').style.display = 'none';
        
        // 메인 카드 보이기
        document.querySelector('.card').style.display = 'block';
    }
}

// 앱 초기화
const app = new QuizApp();
