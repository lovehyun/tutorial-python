# pip install flask_socketio pygame numpy opencv-python

from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import pygame
import cv2
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Pygame Web Game Example')
clock = pygame.time.Clock()
color = (0, 128, 255)
rect = pygame.Rect(30, 30, 60, 60)

keys_pressed = {
    'left': False,
    'right': False,
    'up': False,
    'down': False
}

def generate_frames():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if keys_pressed['left']:
            rect.x -= 5
        if keys_pressed['right']:
            rect.x += 5
        if keys_pressed['up']:
            rect.y -= 5
        if keys_pressed['down']:
            rect.y += 5

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, color, rect)
        pygame.display.flip()

        frame = pygame.surfarray.array3d(screen)
        frame = np.rot90(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        clock.tick(30)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('keydown')
def handle_keydown(key):
    if key == 'left':
        keys_pressed['left'] = True
    elif key == 'right':
        keys_pressed['right'] = True
    elif key == 'up':
        keys_pressed['up'] = True
    elif key == 'down':
        keys_pressed['down'] = True

@socketio.on('keyup')
def handle_keyup(key):
    if key == 'left':
        keys_pressed['left'] = False
    elif key == 'right':
        keys_pressed['right'] = False
    elif key == 'up':
        keys_pressed['up'] = False
    elif key == 'down':
        keys_pressed['down'] = False

if __name__ == '__main__':
    socketio.run(app, debug=True)
