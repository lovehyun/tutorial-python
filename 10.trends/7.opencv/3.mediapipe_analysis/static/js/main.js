let connectionLost = false;

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
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('connection-status').textContent = '연결 끊김';
            document.getElementById('connection-status').className = 'status inactive';
            connectionLost = true;
        });
}

// 페이지 로드시 즉시 호출하고, 이후 주기적으로 호출
fetchPoseSummary();
setInterval(fetchPoseSummary, 3000);  // 3초 간격으로 업데이트

// 페이지 언로드 시 카메라 해제
window.addEventListener('beforeunload', function() {
    fetch('/shutdown');
});
