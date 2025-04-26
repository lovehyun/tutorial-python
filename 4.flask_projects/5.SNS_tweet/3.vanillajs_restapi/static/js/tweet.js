async function submitTweet() {
    const content = document.getElementById('content').value;

    if (!content.trim()) {
        showFlash('내용을 입력하세요.', 'danger');
        return;
    }

    const res = await fetch('/api/tweet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content })
    });

    if (res.ok) {
        showFlash('트윗 작성 완료!', 'success');
        setTimeout(() => {
            window.location.href = '/index.html';
        }, 500);
    } else {
        showFlash('트윗 작성 실패', 'danger');
    }
}
