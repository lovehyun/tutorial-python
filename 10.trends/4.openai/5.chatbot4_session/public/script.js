// public/script.js

document.addEventListener('DOMContentLoaded', async function () {
    const chatContainer = document.getElementById('chat-container');
    const userInputForm = document.getElementById('user-input-form');
    const userInputField = document.getElementById('user-input');
    const loadingIndicator = document.getElementById('loading-indicator');
    const submitButton = document.getElementById('submit-button');
    const currentSessionId = document.getElementById('current-session-id');
    const sessionListContainer = document.getElementById('session-list-container');

    // '전송' 버튼 이벤트
    submitButton.addEventListener('click', function () {
        submitUserInput();
    });

    // '폼' 입력 이벤트
    userInputForm.addEventListener('submit', function (event) {
        event.preventDefault();
        submitUserInput();
    });

    async function submitUserInput() {
        const userInput = userInputField.value;
        const sessionId = currentSessionId.textContent;

        if (userInput.trim() === '') return;

        appendMessage('user', userInput);
        showLoadingIndicator();
        scrollToBottom();

        try {
            const chatGPTResponse = await getChatGPTResponse(sessionId, userInput);
            hideLoadingIndicator();

            // 서버 응답의 개행 문자를 HTML에서 인식하는 <br> 태그로 변환
            const formattedResponse = formatResponseForHTML(chatGPTResponse);
            appendMessage('chatbot', formattedResponse);
        } catch (error) {
            hideLoadingIndicator();
            console.error('Error making ChatGPT API request:', error.message);
            appendMessage('chatbot', '챗봇 응답을 가져오는 도중에 오류가 발생했습니다.');
        }

        userInputField.value = '';
        scrollToBottom();
    }

    function appendMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${role}`;
        messageDiv.innerHTML = '<div class="message-content">' + content + '</div>';
        chatContainer.appendChild(messageDiv);
    }

    async function showSession(sessionId) {
        try {
            const response = await fetch(`/api/session/${sessionId}`);
            const data = await response.json();

            // 화면 지우기
            chatContainer.innerHTML = '';

            // 세션의 대화 내용을 화면에 출력
            data.conversationHistory.forEach((item) => {
                appendMessage(item.role, item.content);
            });

            // 세션 정보를 화면에 갱신
            displaySessionInfo(data);
            
            scrollToBottom();
        } catch (error) {
            console.error('Error loading session:', error.message);
        }
    }

    function showLoadingIndicator() {
        loadingIndicator.style.display = 'flex';
    }

    function hideLoadingIndicator() {
        loadingIndicator.style.display = 'none';
    }

    async function getChatGPTResponse(sessionId, userInput) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sessionId, userInput }),
        });

        const data = await response.json();
        return data.chatGPTResponse;
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // 개행 문자(\n)를 <br> 태그로 변환하는 함수
    function formatResponseForHTML(response) {
        return response.replace(/\n/g, '<br>');
    }

    // 페이지 로딩 시 이전 대화 기록 및 세션 정보를 불러옴
    async function loadChatHistoryAndSession() {
        try {
            // 현재 세션의 대화 내용 불러오기
            const sessionResponse = await fetch('/api/current-session');
            const sessionData = await sessionResponse.json();

            // 현재 세션의 대화 기록을 화면에 출력
            sessionData.conversationHistory.forEach((item) => {
                appendMessage(item.role, item.content);
            });

            // 세션 정보를 화면에 출력
            displaySessionInfo(sessionData);

            scrollToBottom();
        } catch (error) {
            console.error('Error loading chat history and session:', error.message);
        }
    }

    // 페이지 로딩 시 이전 대화 기록과 세션 정보를 불러옴
    await loadChatHistoryAndSession();

    // 세션 정보를 화면에 출력하는 함수 추가
    function displaySessionInfo(sessionData) {
        const sessionIdElement = document.getElementById('current-session-id');
        const sessionDateElement = document.getElementById('current-session-date');

        if (sessionData && sessionData.id && sessionData.start_time) {
            sessionIdElement.textContent = sessionData.id;
            sessionDateElement.textContent = new Date(sessionData.start_time).toLocaleString();
        } else {
            sessionIdElement.textContent = 'N/A';
            sessionDateElement.textContent = 'N/A';
        }
    }

    // 세션 정보 갱신을 위한 함수
    async function updateSessionInfo() {
        try {
            const sessionResponse = await fetch('/api/current-session');
            const sessionData = await sessionResponse.json();
            displaySessionInfo(sessionData);
        } catch (error) {
            console.error('Error updating session info:', error.message);
        }
    }

    // 새로운 대화 세션 시작 버튼 이벤트 리스너 추가
    const newChatButton = document.getElementById('new-chat-button');
    newChatButton.addEventListener('click', async function () {
        try {
            // 새로운 세션 시작 요청
            const response = await fetch('/api/new-session', { method: 'POST' });
            const data = await response.json();

            if (data.success) {
                // 성공적으로 새로운 세션이 시작되면 세션 정보 갱신
                updateSessionInfo();

                // 대화 내용을 모두 삭제하고 화면을 다시 그리기
                clearChatContainer();
            } else {
                console.error('Error starting new session:', data.error);
            }
        } catch (error) {
            console.error('Error starting new session:', error.message);
        }
    });

    // 대화 내용을 모두 삭제하고 화면을 다시 그리는 함수
    function clearChatContainer() {
        chatContainer.innerHTML = ''; // 대화 내용 삭제
        loadAllSessions(); // 세션 목록을 다시 불러와서 화면에 표시
    }

    async function loadAllSessions() {
        try {
            const response = await fetch('/api/all-sessions');
            const data = await response.json();

            // 전체 세션 목록을 화면에 출력
            sessionListContainer.innerHTML = ''; // 기존 목록 제거
            data.allSessions.forEach((session) => {
                appendSession(session);
            });

            // 세션 목록에 클릭 이벤트 리스너 추가
            addSessionClickListeners();
        } catch (error) {
            console.error('Error loading all sessions:', error.message);
        }
    }

    function appendSession(session) {
        const sessionDiv = document.createElement('div');
        sessionDiv.className = 'session-item';
        sessionDiv.innerHTML = `<a href="#" class="session-link" data-session-id="${session.id}">
            <div class="session-id">${session.id}</div>
            <div class="session-start-time">${new Date(session.start_time).toLocaleString()}</div>
        </a>`;
        sessionListContainer.appendChild(sessionDiv);
    }

    // 페이지 로딩 시 전체 세션 목록을 불러오고 표시
    await loadAllSessions();

    // 이전 대화 내용을 클릭했을 때 세션을 가져오는 이벤트 리스너 추가
    function addSessionClickListeners() {
        const sessionLinks = document.querySelectorAll('.session-link');
    
        sessionLinks.forEach((sessionLink) => {
            sessionLink.addEventListener('click', async (event) => {
                const sessionId = sessionLink.dataset.sessionId;
                await showSession(sessionId);
            });
        });
    }

});
