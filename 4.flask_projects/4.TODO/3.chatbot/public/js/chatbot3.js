// 전역 설정값이 없으면 기본값 사용 (현재 서버 자체)
// window.CHATBOT_CONFIG = { API_SERVER: 'https://your-server.com' };
const API_SERVER = window.CHATBOT_CONFIG?.API_SERVER || '';

// 메인 초기화 함수
function initChatbot() {
    loadChatbotStylesheet();
    createChatbotUI();
    registerEventHandlers();
    registerResizeHandler();
}

// DOM이 준비되면 초기화 실행
document.addEventListener('DOMContentLoaded', initChatbot);

// 챗봇 UI 생성 (DOM)
function createChatbotUI() {
    const chatbotHTML = `
        <div class="chatbot-icon" id="chatbotIcon">
            <i class="bi bi-chat-dots-fill"></i>
        </div>
        <div class="chatbot-window" id="chatbotWindow" style="display: none;">
            <div class="resizer" id="resizer"></div>
            <div class="chatbot-header">
                <span>Chatbot</span>
                <button id="closeChatbot">X</button>
            </div>
            <div class="chatbot-body">
                <div class="chatbot-messages" id="chatbotMessages"></div>
                <div class="chatbot-input-container">
                    <input type="text" id="chatbotInput" placeholder="Type a message...">
                    <button id="sendMessage">Send</button>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', chatbotHTML);
}

// CSS 자동 로딩
function loadChatbotStylesheet() {
    const baseURL = window.CHATBOT_CONFIG?.API_SERVER || '.';

    // chatbot용 CSS가 없다면 삽입
    if (!document.querySelector('link[href*="chatbot3_bubble.css"]')) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = `${baseURL}/css/chatbot3_bubble.css`;  // 실제 CSS 경로로 수정
        document.head.appendChild(link);
    }

    // bootstrap-icons도 없으면 삽입
    if (!document.querySelector('link[href*="bootstrap-icons"]')) {
        const bi = document.createElement('link');
        bi.rel = 'stylesheet';
        bi.href = 'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css';
        document.head.appendChild(bi);
    }
}

// 이벤트 등록 (각 챗봇 아이콘 클릭/닫기/메세지전송 등)
function registerEventHandlers() {
    const chatbotIcon = document.getElementById('chatbotIcon');
    const chatbotWindow = document.getElementById('chatbotWindow');
    const closeChatbot = document.getElementById('closeChatbot');
    const sendMessage = document.getElementById('sendMessage');
    const chatbotInput = document.getElementById('chatbotInput');

    // 챗봇 활성화
    chatbotIcon.addEventListener('click', () => {
        chatbotIcon.style.display = 'none';
        chatbotWindow.style.display = 'flex';
    });

    // 챗봇 비활성화
    closeChatbot.addEventListener('click', () => {
        chatbotWindow.style.display = 'none';
        chatbotIcon.style.display = 'flex';
    });

    // 메세지 전송
    sendMessage.addEventListener('click', handleUserMessage);
    chatbotInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleUserMessage();
    });
}

// 메시지 전송 및 수신 처리
async function handleUserMessage() {
    const input = document.getElementById('chatbotInput');
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    input.value = '';

    const botResponse = await sendMessageToServer(message);
    addMessage(botResponse, 'bot');

    // 외부 연동: 예시로 To-Do 갱신
    if (typeof loadTodos === 'function') {
        loadTodos();
    }
}

// 메시지 추가
function addMessage(message, sender = 'user') {
    const container = document.getElementById('chatbotMessages');
    const formatted = message.replace(/\n/g, '<br>');

    const messageElement = document.createElement('div');
    messageElement.innerHTML = sender === 'user'
        ? `<i class="bi bi-person"></i> ${formatted}`
        : `<i class="bi bi-robot"></i> ${formatted}`;
    messageElement.classList.add(sender);

    container.appendChild(messageElement);
    container.scrollTop = container.scrollHeight;
}

// 서버에 질문 전송
async function sendMessageToServer(question) {
    try {
        const res = await fetch(`${API_SERVER}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });
        const data = await res.json();
        return data.answer || '응답이 없습니다.';
    } catch (e) {
        console.error('서버 오류:', e);
        return '서버와 연결할 수 없습니다.';
    }
}

// 리사이즈 핸들러 등록
function registerResizeHandler() {
    const chatbotWindow = document.getElementById('chatbotWindow');
    const resizer = document.getElementById('resizer');

    let isResizing = false;
    let startX, startY, startWidth, startHeight;

    resizer.addEventListener('mousedown', (e) => {
        e.preventDefault();
        isResizing = true;
        startX = e.clientX;
        startY = e.clientY;
        const rect = chatbotWindow.getBoundingClientRect();
        startWidth = rect.width;
        startHeight = rect.height;
    });

    document.addEventListener('mousemove', (e) => {
        if (!isResizing) return;

        const dx = startX - e.clientX;  // 왼쪽 방향 드래그
        const dy = startY - e.clientY;  // 위쪽 방향 드래그
        chatbotWindow.style.width = Math.max(250, startWidth + dx) + 'px';
        chatbotWindow.style.height = Math.max(300, startHeight + dy) + 'px';
    });

    document.addEventListener('mouseup', () => {
        isResizing = false;
    });
}
