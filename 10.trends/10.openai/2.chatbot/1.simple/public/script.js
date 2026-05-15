document.addEventListener('DOMContentLoaded', function () {
    const chatContainer = document.getElementById('chat-container');
    const userInputForm = document.getElementById('user-input-form');
    const userInputField = document.getElementById('user-input');

    userInputForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const userInput = userInputField.value;
        if (userInput.trim() === '') return;

        appendMessage('user', userInput);

        try {
            const chatGPTResponse = await getChatGPTResponse(userInput);
            appendMessage('chatbot', chatGPTResponse);
        } catch (error) {
            console.error('Error making ChatGPT API request:', error.message);
            appendMessage('chatbot', '챗봇 응답을 가져오는 도중에 오류가 발생했습니다.');
        }

        userInputField.value = '';
    });

    function appendMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', role);
        messageDiv.textContent = content;
        chatContainer.appendChild(messageDiv);
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
});
