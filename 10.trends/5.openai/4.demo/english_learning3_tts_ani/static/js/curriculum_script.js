document.getElementById('chatForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const userInput = document.getElementById('user_input').value;
    
    // 사용자 입력 클리어
    document.getElementById('user_input').value = '';

    // 채팅 로그에 학생 메세지 추가
    const chatLog = document.getElementById('chatlog');
    chatLog.innerHTML += `<div><strong>학생:</strong> ${userInput}</div>`;

    // chatlog 자동 스크롤
    chatLog.scrollTop = chatLog.scrollHeight;

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
        // 백엔드에서 받은 데이터를 채팅 로그에 추가
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

const recordButton = document.getElementById('recordButton');
let mediaRecorder;
let audioChunks = [];

recordButton.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        recordButton.textContent = "Speak";
    } else {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();
                recordButton.textContent = "녹음 중지";

                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    audioChunks = [];

                    const formData = new FormData();
                    formData.append('audio_file', audioBlob);

                    fetch('/speech-to-text', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        // 음성 인식 결과를 텍스트 입력창에 표시하고 자동으로 제출
                        document.getElementById('user_input').value = data.transcript;
                        document.getElementById('chatForm').dispatchEvent(new Event('submit'));
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                };
            })
            .catch(error => {
                console.error('Error accessing media devices.', error);
            });
    }
});
