from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import random
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

rooms = {}
users = {}
terrain = []

colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']

def generate_terrain():
    degree = random.randint(2, 8)  # Random polynomial degree between 2 and 8
    coefficients = [random.uniform(-1, 1) for _ in range(degree + 1)]
    points = []

    for x in range(0, 801, 10):  # Canvas width is 800
        y = sum(coeff * (x ** idx) for idx, coeff in enumerate(coefficients))
        y = max(min(y, 300), 150)  # Clamp y values between 150 and 300
        points.append({'x': x, 'y': y})

    print(f"Generated terrain with degree {degree}: {points}")  # 콘솔에 지형 출력
    return points

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    global terrain
    username = data['username']
    room = data['room']
    color = random.choice(colors)
    join_room(room)
    rooms[username] = room
    users[username] = {'username': username, 'room': room, 'color': color, 'position': {'top': '50%', 'left': '50%'}}
    
    # If terrain is not generated yet, generate it
    if not terrain:
        terrain = generate_terrain()

    print("User joined:", username, "Terrain:", terrain)  # 콘솔에 사용자와 지형 출력

    # Broadcast to existing users about the new user
    emit('new_user', {'user': users[username], 'terrain': terrain}, room=room, include_self=False)

    # Send all existing users to the new user along with the terrain
    emit('existing_users', {'users': list(users.values()), 'terrain': terrain}, room=request.sid)

    emit('message', {'msg': f'{username} has joined the room.'}, room=room)

@socketio.on('move')
def on_move(data):
    username = data['username']
    direction = data['direction']
    room = rooms[username]

    # Update the user's position
    if direction == 'left':
        users[username]['position']['left'] = str(max(int(users[username]['position']['left'].replace('%', '')) - 5, 0)) + '%'
    elif direction == 'right':
        users[username]['position']['left'] = str(min(int(users[username]['position']['left'].replace('%', '')) + 5, 95)) + '%'

    emit('move', {'username': username, 'direction': direction, 'position': users[username]['position']}, room=room)

@socketio.on('attack')
def on_attack(data):
    room = rooms[data['username']]
    emit('attack', data, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
