const socket = io();
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const statusDisplay = document.getElementById('status');
const clearButton = document.getElementById('clearCanvas');
const wordDisplay = document.getElementById('wordDisplay');
const guessInput = document.getElementById('guessInput');

let drawing = false;
let isDrawer = false;
let drawer = null;

let currentX = 0;
let currentY = 0;

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);
clearButton.addEventListener('click', clearCanvas);

clearButton.disabled = true;
guessInput.disabled = false;

function startDrawing(e) {
    if (!isDrawer) return;
    drawing = true;
    [currentX, currentY] = [e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop];
    ctx.beginPath();
    ctx.moveTo(currentX, currentY);
    socket.emit('startDrawing', {
        x: currentX,
        y: currentY
    });
    console.log(`Start drawing at: (${currentX}, ${currentY})`);
}

function draw(e) {
    if (!drawing) return;
    const x = e.clientX - canvas.offsetLeft;
    const y = e.clientY - canvas.offsetTop;

    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#000000';

    ctx.lineTo(x, y);
    ctx.stroke();
    [currentX, currentY] = [x, y];

    socket.emit('drawing', {
        x1: currentX,
        y1: currentY,
        x2: x,
        y2: y
    });
}

function stopDrawing() {
    if (!isDrawer) return;
    drawing = false;
    ctx.beginPath();
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    socket.emit('clearCanvas');
}

socket.on('startDrawing', (data) => {
    console.log(`Received start drawing at: (${data.x}, ${data.y})`);
    [currentX, currentY] = [data.x, data.y];
    ctx.beginPath();
    ctx.moveTo(currentX, currentY);
});

socket.on('drawing', (data) => {
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#000000';

    ctx.lineTo(data.x2, data.y2);
    ctx.stroke();
    [currentX, currentY] = [data.x2, data.y2];
});

socket.on('newWord', (word) => {
    console.log(`[${new Date().toISOString()}] newWord event received: ${word}`);
    if (isDrawer) {
        alert('You are drawing: ' + word);
        wordDisplay.textContent = 'You are drawing: ' + word;
    }
});

guessInput.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') {
        socket.emit('guess', e.target.value);
        e.target.value = '';
    }
});

socket.on('guess', (data) => {
    if (isDrawer) {
        guessInput.value += `Player ${data.player}: ${data.guess}\n`;
        guessInput.scrollTop = guessInput.scrollHeight; // 자동으로 스크롤
    }
});

socket.on('correctGuess', (id) => {
    alert('Player ' + id + ' guessed correctly!');
    if (!isDrawer) {
        wordDisplay.textContent = '';
    }
});

socket.on('drawerSelected', (drawerId) => {
    drawer = drawerId;
    console.log(`[${new Date().toISOString()}] drawerSelected message received: ${drawerId}`);
    if (drawerId === socket.id) {
        statusDisplay.textContent = 'You are drawing!';
        isDrawer = true;
        clearButton.disabled = false;
        guessInput.disabled = true;
        guessInput.value = ''; // 내 턴일 때 입력 필드를 비웁니다.
    } else {
        statusDisplay.textContent = 'Guess the word!';
        isDrawer = false;
        clearButton.disabled = true;
        guessInput.disabled = false;
        wordDisplay.textContent = '';
        guessInput.value = ''; // 내 턴일 때 입력 필드를 비웁니다.
    }
});

socket.on('clearCanvas', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
});
