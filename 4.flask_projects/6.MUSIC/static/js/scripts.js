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
});
