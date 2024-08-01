document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io();
    var selectedRoom = null;

    socket.on('room_full', (data) => {
        console.log(`Room ${data.room} is full!`);
        alert(`Room ${data.room} is full! Please choose another room.`);
        document.getElementById('usernameOverlay').style.display = 'none';  // 이름 입력 창 숨기기
    });

    document.querySelectorAll('.room-box').forEach(box => {
        box.addEventListener('click', () => {
            selectedRoom = box.getAttribute('data-room');
            document.getElementById('usernameOverlay').style.display = 'flex';
        });
    });

    document.getElementById('joinRoomButton').addEventListener('click', joinRoom);

    document.getElementById('usernameInput').addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            joinRoom();
        }
    });

    function joinRoom() {
        let username = document.getElementById('usernameInput').value.trim();
        if (!username) {
            alert("Username cannot be empty.");
            return;
        }
        console.log(`Attempting to join room: ${selectedRoom} as user: ${username}`);

        // Create a form and submit it via POST
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/game/${selectedRoom}`;
        const usernameInput = document.createElement('input');
        usernameInput.type = 'hidden';
        usernameInput.name = 'username';
        usernameInput.value = username;
        form.appendChild(usernameInput);
        document.body.appendChild(form);
        form.submit();
    }

    socket.on('connect', () => {
        console.log('Connected to server');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
    });

    socket.on('connect_error', (error) => {
        console.log('Connection error:', error);
    });
});
