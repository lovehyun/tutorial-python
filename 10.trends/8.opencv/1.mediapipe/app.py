from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import atexit

app = Flask(__name__)

# Pose Estimation 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)  # 웹캠 열기

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        # RGB 변환 후 포즈 인식
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # 결과 그리기
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

        # 프레임 인코딩
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # multipart로 스트리밍
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/shutdown')
def shutdown():
    cap.release()
    return "Camera Released"

@atexit.register
def release_camera_on_exit():
    if cap.isOpened():
        print("🔒 Cleaning up: Releasing webcam...")
        cap.release()
        print("✅ Webcam released.")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
