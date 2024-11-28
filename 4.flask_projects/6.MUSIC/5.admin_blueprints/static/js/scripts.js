document.addEventListener('DOMContentLoaded', function() {
    const notificationIcon = document.getElementById('notification-icon');
    if (notificationIcon) {
        notificationIcon.addEventListener('click', function() {
            fetch('/notifications')
                .then(response => response.json())
                .then(data => {
                    // Handle notification data
                });
        });
    }

    // 좋아요 버튼 클릭 이벤트 핸들러
    const likeButtons = document.querySelectorAll('.like-button');
    likeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const userId = document.body.dataset.userId;
            if (!userId) {
                event.preventDefault();
                alert('로그인이 필요합니다.');
            }
        });
    });

    // 댓글 폼 제출 이벤트 핸들러
    const commentForms = document.querySelectorAll('.comment-form');
    commentForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const userId = document.body.dataset.userId;
            if (!userId) {
                event.preventDefault();
                alert('로그인이 필요합니다.');
            }
        });
    });

    // 해시태그 폼 제출 이벤트 핸들러
    const hashtagForms = document.querySelectorAll('.hashtags form');
    hashtagForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const userId = document.body.dataset.userId;
            if (!userId) {
                event.preventDefault();
                alert('로그인이 필요합니다.');
            }
        });
    });
});
