const API_SERVER = '';

document.addEventListener("DOMContentLoaded", function() {
    const chatbotIcon = document.getElementById('chatbotIcon');
    const chatbotWindow = document.getElementById('chatbotWindow');
    const closeChatbot = document.getElementById('closeChatbot');
    const sendMessage = document.getElementById('sendMessage');
    const chatbotMessages = document.getElementById('chatbotMessages');
    const chatbotInput = document.getElementById('chatbotInput');

    chatbotIcon.addEventListener('click', () => {
        chatbotIcon.style.display = 'none';
        chatbotWindow.style.display = 'flex';
    });

    closeChatbot.addEventListener('click', () => {
        chatbotWindow.style.display = 'none';
        chatbotIcon.style.display = 'flex';
    });

    sendMessage.addEventListener('click', handleUserMessage);
    chatbotInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') handleUserMessage();
    });

    function addMessage(message, sender = 'user') {
        const messageElement = document.createElement('div');
        messageElement.innerHTML = sender === 'user'
            ? `<i class="bi bi-person"></i> ${message}`
            : `<i class="bi bi-robot"></i> ${message}`;
        messageElement.classList.add(sender);
        chatbotMessages.appendChild(messageElement);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    async function handleUserMessage() {
        const message = chatbotInput.value.trim();
        if (message) {
            addMessage(message, 'user');
            chatbotInput.value = '';

            const botResponse = await sendMessageToServer(message);
            addMessage(botResponse, 'bot');
        }
    }

    async function sendMessageToServer(question) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question })
            });
            const data = await response.json();
            return data.answer;
        } catch (error) {
            console.error('서버와의 연결 오류:', error);
            return '서버와 연결할 수 없습니다.';
        }
    }
});
