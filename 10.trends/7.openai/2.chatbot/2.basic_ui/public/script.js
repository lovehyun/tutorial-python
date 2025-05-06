document.addEventListener('DOMContentLoaded', function () {
    const chatContainer = document.getElementById('chat-container');
    const userInputForm = document.getElementById('user-input-form');
    const userInputField = document.getElementById('user-input');
    const submitButton = document.getElementById('submit-button');

    let loadingMessageDiv = null;

    submitButton.addEventListener('click', function () {
        submitUserInput();
    });

    userInputForm.addEventListener('submit', function (event) {
        event.preventDefault();
        submitUserInput();
    });

    async function submitUserInput() {
        const userInput = userInputField.value;
        if (userInput.trim() === '') return;

        appendMessage('user', userInput);
        showLoadingIndicator();

        try {
            const chatGPTResponse = await getChatGPTResponse(userInput);
            hideLoadingIndicator();

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
        scrollToBottom();
    }

    function showLoadingIndicator() {
        loadingMessageDiv = document.createElement('div');
        loadingMessageDiv.className = 'chat-message chatbot';
        loadingMessageDiv.innerHTML = `
            <div class="message-content">
                <span class="loading-dots"></span> 생각 중...
            </div>
        `;
        chatContainer.appendChild(loadingMessageDiv);
        scrollToBottom();
    }

    function hideLoadingIndicator() {
        if (loadingMessageDiv) {
            loadingMessageDiv.remove();
            loadingMessageDiv = null;
        }
    }

    async function getChatGPTResponse(userInput) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userInput }),
        });

        const data = await response.json();
        return data.chatGPTResponse;
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function formatResponseForHTML(response) {
        return response.replace(/\n/g, '<br>');
    }
});
