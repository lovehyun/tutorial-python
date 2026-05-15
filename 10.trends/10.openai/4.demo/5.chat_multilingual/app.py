import json
import os
import logging

from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO
from openai import OpenAI
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

app = Flask(__name__, static_folder='public')
socketio = SocketIO(app, cors_allowed_origins="*")

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
messages = []
user_map = {}  # socket.id -> {username, language}
typing_users = set()

def translate_message(text, target_lang):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"Translate to {target_lang}:"},
                {"role": "user", "content": text}
            ]
        )
        translated = response.choices[0].message.content
        print(f"🔄 Translation: {text} -> {translated} ({target_lang})")
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@socketio.on('connect')
def handle_connect():
    total_users = len(socketio.server.eio.sockets)
    print(f"✅ New user connected! Socket ID: {request.sid}, Total users: {total_users}")
    socketio.emit('user count', total_users)

@socketio.on('user joined')
def handle_join(username):
    user_map[request.sid] = {'username': username, 'language': 'ko'}
    print(f"👤 User joined: {username} (id: {request.sid})")

@socketio.on('set language')
def handle_language(lang):
    if request.sid in user_map:
        user_map[request.sid]['language'] = lang
        print(f"🌍 Language set for {user_map[request.sid]['username']}: {lang}")

@socketio.on('typing')
def handle_typing():
    username = user_map.get(request.sid, {}).get('username', 'Unknown user')
    print(f"✍️ {username} is typing...")
    typing_users.add(username)
    socketio.emit('typing', username, skip_sid=request.sid)

@socketio.on('stop typing')
def handle_stop_typing():
    username = user_map.get(request.sid, {}).get('username', 'Unknown user')
    print(f"✋ {username} has stopped typing...")
    typing_users.discard(username)
    socketio.emit('stop typing', username, skip_sid=request.sid)

@socketio.on('chat message')
def handle_message(data):
    sender = user_map.get(request.sid, {})
    unread_users = [sid for sid in user_map if sid != request.sid]
    
    message_data = {
        'username': data['username'],
        'message': data['message'],
        'timestamp': data['timestamp'],
        'unread_users': unread_users
    }
    messages.append(message_data)

    # 각 사용자의 언어로 번역하여 전송
    for sid in user_map:
        target_lang = user_map[sid]['language']
        if sid != request.sid:
            translated_msg = translate_message(data['message'], target_lang)
            socketio.emit('chat message', {
                'username': data['username'],
                'message': translated_msg,
                'timestamp': data['timestamp'],
                'unreadUsers': unread_users
            }, room=sid)

@socketio.on('read message')
def handle_read(data):
    msg_idx = next((i for i, m in enumerate(messages) if m['timestamp'] == data['timestamp']), -1)
    if msg_idx != -1:
        messages[msg_idx]['unread_users'].remove(request.sid)
        socketio.emit('update read receipt', {
            'timestamp': data['timestamp'],
            'unreadUsers': messages[msg_idx]['unread_users']
        })

@socketio.on('disconnect')
def handle_disconnect():
    username = user_map.get(request.sid, {}).get('username', 'Unknown user')
    print(f"❌ User disconnected: {username} (ID: {request.sid})")
    
    if request.sid in user_map:
        del user_map[request.sid]
    
    for msg in messages:
        if request.sid in msg['unread_users']:
            msg['unread_users'].remove(request.sid)
    
    socketio.emit('user count', len(socketio.server.eio.sockets))

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
