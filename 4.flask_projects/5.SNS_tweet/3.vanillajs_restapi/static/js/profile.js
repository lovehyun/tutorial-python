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

document.addEventListener('DOMContentLoaded', renderProfile);
