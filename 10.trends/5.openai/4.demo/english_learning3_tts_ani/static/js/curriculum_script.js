document.getElementById('chatForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const userInput = document.getElementById('user_input').value;
    
    // 사용자 입력 클리어
    document.getElementById('user_input').value = '';

    // 백엔드에 요청
    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'user_input': userInput
        })
    })
    .then(response => response.json())
    .then(data => {
        const chatLog = document.getElementById('chatlog');
        chatLog.innerHTML += `<div><strong>학생:</strong> ${userInput}</div>`;
        chatLog.innerHTML += `<div><strong>ChatGPT:</strong> ${data.response}</div>`;

        // chatlog 자동 스크롤
        chatLog.scrollTop = chatLog.scrollHeight;

        // TTS 기능 추가
        const ttsAudio = document.getElementById('ttsAudio');
        ttsAudio.src = `/audio/${data.audio_path}`;
        ttsAudio.style.display = 'block';
        ttsAudio.play();

        ttsAudio.onplay = () => {
            anime({
                targets: '#mouth',
                scaleY: [
                    { value: 1.5, duration: 200 },
                    { value: 1, duration: 200 }
                ],
                loop: true,
                easing: 'easeInOutSine'
            });
        };

        ttsAudio.onpause = ttsAudio.onended = () => {
            anime.remove('#mouth');
            document.getElementById('mouth').style.transform = 'translateX(-50%) scaleY(1)';
        };
    });
});
