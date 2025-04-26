async function renderProfile() {
    const user = await fetchMe();
    if (!user) {
        window.location.href = '/login.html';
        return;
    }

    document.getElementById('profile-username').value = user.username;
    document.getElementById('profile-email').value = user.email;
}

async function updateProfile() {
    const username = document.getElementById('profile-username').value;
    const email = document.getElementById('profile-email').value;

    const res = await fetch('/api/profile/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email })
    });

    if (res.ok) {
        showFlash('프로필이 수정되었습니다.', 'success');
    } else {
        const error = await res.json();
        showFlash(error.error || '프로필 수정 실패', 'danger');
    }
}

async function updatePassword() {
    const currentPassword = document.getElementById('current-password').value;
    const newPassword = document.getElementById('new-password').value;

    if (!currentPassword || !newPassword) {
        showFlash('모든 필드를 입력하세요.', 'danger');
        return;
    }

    const res = await fetch('/api/profile/password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ current_password: currentPassword, new_password: newPassword })
    });

    if (res.ok) {
        showFlash('비밀번호가 변경되었습니다.', 'success');
        document.getElementById('password-form').reset();
    } else {
        const error = await res.json();
        showFlash(error.error || '비밀번호 변경 실패', 'danger');
    }
}

document.addEventListener('DOMContentLoaded', renderProfile);
