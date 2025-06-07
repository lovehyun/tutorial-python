from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app, logger=True, engineio_logger=True)

rooms = {f'room{i}': [] for i in range(1, 9)}
users = {}

colors = ['red', 'blue', 'green', 'purple', 'orange']

terrain_data = {
    'room1': [{'x': x, 'y': 200} for x in range(0, 801, 10)],
    'room2': [{'x': x, 'y': 300 if x < 400 else 150} for x in range(0, 801, 10)],
    'room3': [{'x': x, 'y': 150 if (200 < x < 400) or (600 < x < 800) else 300} for x in range(0, 801, 10)],
    'room4': [{'x': x, 'y': 150 if (150 < x < 250) or (400 < x < 500) or (650 < x < 750) else 300} for x in range(0, 801, 10)],
    'room5': [{'x': x, 'y': 150 + (x % 400) * 0.375 if (x // 400) % 2 == 0 else 300 - (x % 400) * 0.375} for x in range(0, 801, 10)],
    'room6': [{'x': x, 'y': 200 + (x % 400) * 0.25 if (x // 400) % 2 == 0 else 200 - (x % 400) * 0.25} for x in range(0, 801, 10)],
    'room7': [{'x': x, 'y': 150 + (x % 400) * 0.5 if (x // 400) % 2 == 0 else 300 - (x % 400) * 0.5} for x in range(0, 801, 10)],
    'room8': [{'x': x, 'y': 200 + (x % 400) * 0.75 if (x // 400) % 2 == 0 else 200 - (x % 400) * 0.75} for x in range(0, 801, 10)],
}

@app.route('/')
def index():
    return render_template('index.html', rooms=[{'name': room, 'count': len(rooms[room])} for room in rooms])

@app.route('/game/<room>', methods=['POST'])
def game(room):
    username = request.form.get('username')
    if not username:
        return redirect(url_for('index'))
    return render_template('game.html', username=username, room=room)

@socketio.on('check_room')
def check_room(data):
    room = data['room']
    if len(rooms[room]) >= 4:
        emit('room_full', {'room': room})
    else:
        emit('room_available', {'room': room})

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    if len(rooms[room]) >= 4:
        emit('room_full', {'room': room})
        return

    color = random.choice(colors)
    join_room(room)
    rooms[room].append(username)
    users[username] = {'username': username, 'room': room, 'color': color, 'position': {'top': '300px', 'left': '400px'}}
    terrain = terrain_data[room]

    print(f"User {username} joined room {room}. Color: {color}")

    emit('new_user', {'user': users[username], 'terrain': terrain, 'room': room, 'count': len(rooms[room])}, room=room, include_self=False)
    print(f"Emitting new_user to room {room} with user {username}")

    emit('existing_users', {'users': [users[u] for u in rooms[room]], 'terrain': terrain, 'room': room}, room=request.sid)
    print(f"Emitting existing_users to {username}")

    emit('message', {'msg': f'{username} has joined room {room}.'}, room=room)
    print(f"Emitting message to room {room}: {username} has joined room {room}.")

    emit('joined_room', {'username': username, 'room': room}, room=request.sid)
    print(f"Emitting joined_room to {username}")

@socketio.on('move')
def on_move(data):
    username = data['username']
    direction = data['direction']
    
    if username not in users:
        print(f"Error: {username} not found in users")
        return
    
    room = users[username]['room']

    if direction == 'left':
        users[username]['position']['left'] = str(max(int(users[username]['position']['left'].replace('px', '')) - 5, 0)) + 'px'
    elif direction == 'right':
        users[username]['position']['left'] = str(min(int(users[username]['position']['left'].replace('px', '')) + 5, 795)) + 'px'

    emit('move', {'username': username, 'direction': direction, 'position': users[username]['position'], 'color': users[username]['color']}, room=room)
    print(f"Emitting move: {username} moved {direction} to {users[username]['position']}")

@socketio.on('attack')
def on_attack(data):
    username = data['username']
    if username not in users:
        print(f"Error: {username} not found in users")
        return
    
    room = users[username]['room']
    emit('attack', data, room=room)
    print(f"Emitting attack: {username} attacked with power {data['power']} in room {room}")

if __name__ == '__main__':
    socketio.run(app, debug=True)
