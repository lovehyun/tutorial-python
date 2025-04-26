// 로그인 여부에 따라 네비게이션 메뉴 제어
async function setupNav() {
    const user = await fetchMe();

    if (user) {
        document.getElementById('nav-login').style.display = 'none';
        document.getElementById('nav-logout').style.display = 'inline';
        document.getElementById('nav-profile').style.display = 'inline';
        document.getElementById('nav-tweet').style.display = 'inline';
    } else {
        document.getElementById('nav-login').style.display = 'inline';
        document.getElementById('nav-logout').style.display = 'none';
        document.getElementById('nav-profile').style.display = 'none';
        document.getElementById('nav-tweet').style.display = 'none';
    }
}

// 플래시 메시지 출력
function showFlash(message, type='success') {
    const flash = document.getElementById('flash-message');
    flash.innerHTML = `<li class="${type}">${message}</li>`;
    setTimeout(() => {
        flash.innerHTML = '';
    }, 3000);
}

// API로 현재 사용자 정보 가져오기
async function fetchMe() {
    const res = await fetch('/api/me');
    return await res.json();
}

// 로그아웃 처리
async function logout() {
    await fetch('/api/logout', { method: 'POST' });
    window.location.href = '/login.html';
}

// 페이지 로드 시 메뉴 설정
document.addEventListener('DOMContentLoaded', setupNav);
