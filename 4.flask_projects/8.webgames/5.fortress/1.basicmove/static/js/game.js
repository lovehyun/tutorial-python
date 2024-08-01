document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io();
    const config = window.gameConfig;
    var username = config.username;
    var room = config.room;
    var terrain = [];

    console.log(`Joining room: ${room} as user: ${username}`);
    socket.emit('join', {username: username, room: room});

    socket.on('message', (data) => {
        console.log(`Message received: ${data.msg}`);
        alert(data.msg);
    });

    socket.on('new_user', (data) => {
        console.log('New user:', data);
        terrain = data.terrain;
        console.log('Terrain received (new_user):', terrain);
        drawTerrain(terrain);
        addTank(data.user.username, data.user.color, data.user.position.top, data.user.position.left);
        updateRoomTitle(data.room, data.count);
    });

    socket.on('existing_users', (data) => {
        console.log('Existing users:', data);
        terrain = data.terrain;
        console.log('Terrain received (existing_users):', terrain);
        drawTerrain(terrain);
        data.users.forEach(user => {
            addTank(user.username, user.color, user.position.top, user.position.left);
        });
        updateRoomTitle(data.room, data.users.length);
    });

    socket.on('move', (data) => {
        moveTank(data.username, data.direction, data.position);
    });

    socket.on('attack', (data) => {
        console.log('Attack:', data);
        attack(data.username, data.power);
    });

    socket.on('connect', () => {
        console.log('Connected to server');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
    });

    socket.on('connect_error', (error) => {
        console.log('Connection error:', error);
    });

    function drawTerrain(terrain) {
        console.log('Drawing terrain:', terrain);
        const terrainCanvas = document.getElementById('terrain');
        if (!terrainCanvas) {
            console.error('Canvas element not found!');
            return;
        }

        const ctx = terrainCanvas.getContext('2d');
        if (!ctx) {
            console.error('Failed to get canvas context!');
            return;
        }

        const width = terrainCanvas.width;
        const height = terrainCanvas.height;

        ctx.clearRect(0, 0, width, height);
        ctx.fillStyle = '#87CEEB'; // Light blue for sky
        ctx.fillRect(0, 0, width, height);

        ctx.beginPath();
        ctx.moveTo(0, height);

        terrain.forEach(point => {
            ctx.lineTo(point.x, point.y);
        });

        ctx.lineTo(width, height);
        ctx.closePath();
        ctx.fillStyle = '#654321'; // Brown for terrain
        ctx.fill();

        console.log('Terrain drawn on canvas.');
    }

    function addTank(username, color, top='300px', left='400px') {
        if (!username) {
            console.error('Invalid username:', username);
            return;
        }
        const gameArea = document.getElementById('gameArea');
        let tank = document.getElementById(username);
        if (!tank) {
            tank = document.createElement('div');
            tank.classList.add('tank');
            tank.id = username;
            tank.style.backgroundColor = color;
            tank.style.left = left;
            gameArea.appendChild(tank);
        } else {
            tank.style.backgroundColor = color;
            tank.style.left = left;
        }
        
        const leftPx = parseInt(left.replace('px', ''));
        const terrainY = getTerrainY(leftPx);
        tank.style.top = `${terrainY - tank.offsetHeight}px`; // 탱크 높이 보정

        tank.innerHTML = username;
        tank.style.color = 'white';
        tank.style.textAlign = 'center';
        tank.style.lineHeight = '40px';
        
        console.log(`Tank added or updated: ${username}, Color: ${color}`);
    }

    function moveTank(username, direction, position) {
        const tank = document.getElementById(username);
        if (!tank) {
            console.error(`Tank for user ${username} not found!`);
            return;
        }
        const step = 5;
        let left = parseInt(tank.style.left.replace('px', ''));

        if (direction === 'left') {
            left = Math.max(left - step, 0);
        } else if (direction === 'right') {
            left = Math.min(left + step, 760);
        }

        tank.style.left = `${left}px`;
        const terrainY = getTerrainY(left);
        tank.style.top = `${terrainY - tank.offsetHeight}px`;  // 탱크 높이 보정
    }

    function getTerrainY(x) {
        const point = terrain.find(point => point.x >= x);
        return point ? point.y : 150;
    }

    function attack(username, power) {
        console.log(`${username} attacks with power ${power}`);
    }

    function updateRoomTitle(room, count) {
        document.getElementById('roomTitle').innerText = `Room: ${room} (${count}/4)`;
    }

    document.addEventListener('keydown', (event) => {
        if (event.key === 'ArrowLeft') {
            socket.emit('move', {username: username, direction: 'left'});
        } else if (event.key === 'ArrowRight') {
            socket.emit('move', {username: username, direction: 'right'});
        } else if (event.key === ' ') {
            socket.emit('attack', {username: username, power: 10});
        }
    });
});
