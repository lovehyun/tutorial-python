async function register() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const res = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
    });

    if (res.ok) {
        showFlash('회원가입 성공! 로그인 해주세요.', 'success');
        setTimeout(() => {
            window.location.href = '/login.html';
        }, 500);
    } else {
        const error = await res.json();
        showFlash(error.error || '회원가입 실패', 'danger');
    }
}
