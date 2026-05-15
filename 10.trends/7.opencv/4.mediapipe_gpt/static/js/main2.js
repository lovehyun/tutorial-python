let connectionLost = false;
let lastUpdateTime = new Date();
let lastPoseTime = null;

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
            document.getElementById('gpt-analysis').innerText = data.description;
            if (data.based_on_time) {
                lastPoseTime = new Date(data.based_on_time);
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
    if (!lastPoseTime) {
        statusElem.innerText = '분석 대기 중';
        return;
    }

    const now = new Date();
    const elapsedSeconds = Math.floor((now - lastPoseTime) / 1000);

    let timeText = '';
    if (elapsedSeconds < 60) {
        timeText = `${elapsedSeconds}초 전`;
    } else {
        timeText = `${Math.floor(elapsedSeconds / 60)}분 전`;
    }

    const statusElem = document.getElementById('update-time');
    statusElem.innerText = `분석 기준: ${timeText}`;
}

// 페이지 로드시 즉시 호출하고, 이후 주기적으로 호출
fetchPoseSummary();
setInterval(fetchPoseSummary, 1000);  // 1초 간격으로 업데이트
setInterval(updateTimestamp, 1000);   // 경과 시간 갱신

// 페이지 언로드 시 카메라 해제
window.addEventListener('beforeunload', function() {
    fetch('/shutdown');
});
