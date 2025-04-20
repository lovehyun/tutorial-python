let connectionLost = false;
let lastUpdateTime = new Date();

function fetchPoseSummary() {
    fetch('/pose_summary')
        .then(response => {
            if (!response.ok) {
                throw new Error('서버 연결 실패');
            }
            if (connectionLost) {
                document.getElementById('connection-status').textContent = '연결됨';
                document.getElementById('connection-status').className = 'status active';
                connectionLost = false;
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('pose-text').innerText = data.summary;
            
            // GPT 분석 결과가 변경되었을 때만 업데이트 시간 갱신
            const currentGptText = document.getElementById('gpt-analysis').innerText;
            if (currentGptText !== data.description) {
                document.getElementById('gpt-analysis').innerText = data.description;
                lastUpdateTime = new Date();
                updateTimestamp();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('connection-status').textContent = '연결 끊김';
            document.getElementById('connection-status').className = 'status inactive';
            connectionLost = true;
        });
}

function updateTimestamp() {
    const now = new Date();
    const elapsedSeconds = Math.floor((now - lastUpdateTime) / 1000);
    
    let timeText;
    if (elapsedSeconds < 60) {
        timeText = `${elapsedSeconds}초 전`;
    } else if (elapsedSeconds < 3600) {
        timeText = `${Math.floor(elapsedSeconds / 60)}분 전`;
    } else {
        timeText = `${Math.floor(elapsedSeconds / 3600)}시간 전`;
    }
    
    document.getElementById('update-time').innerText = `마지막 업데이트: ${timeText}`;
}

// 페이지 로드시 즉시 호출하고, 이후 주기적으로 호출
fetchPoseSummary();
setInterval(fetchPoseSummary, 1000);  // 1초 간격으로 업데이트
setInterval(updateTimestamp, 5000);   // 5초마다 타임스탬프 업데이트

// 페이지 언로드 시 카메라 해제
window.addEventListener('beforeunload', function() {
    fetch('/shutdown');
});
