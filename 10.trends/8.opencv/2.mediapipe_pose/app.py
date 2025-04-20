from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
import time
import atexit

app = Flask(__name__)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
latest_pose_summary = "No pose detected yet."

def summarize_pose(landmarks, frame_width=640, frame_height=480):
    # 상반신 위주 관절만 추출
    key_joints = {
        "left_shoulder": landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
        "left_elbow": landmarks[mp_pose.PoseLandmark.LEFT_ELBOW],
        "left_wrist": landmarks[mp_pose.PoseLandmark.LEFT_WRIST],
        "right_shoulder": landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER],
        "right_elbow": landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW],
        "right_wrist": landmarks[mp_pose.PoseLandmark.RIGHT_WRIST],
    }

    summary = []
    visible_parts = 0
    
    # 주요 관절 visibility 확인 (0.5 이상이면 신뢰할 수 있는 것으로 간주)
    for name, lm in key_joints.items():
        if lm.visibility > 0.5:  # visibility 임계값 추가
            # 정규화된 좌표(0.0~1.0, 1.0보다 크면 화면 밖)를 픽셀 좌표로 변환
            pixel_x = int(lm.x * frame_width)
            pixel_y = int(lm.y * frame_height)
            summary.append(f"{name}: 정규화({lm.x:.2f}, {lm.y:.2f}) / 픽셀({pixel_x}, {pixel_y})")
            visible_parts += 1
        else:
            summary.append(f"{name}: not visible")
    
    if visible_parts == 0:
        return "주요 신체 부위가 감지되지 않았습니다. 상반신이 보이도록 카메라 위치를 조정해주세요."
        
    return "\n".join(summary)

def generate_frames():
    global latest_pose_summary
    last_update_time = time.time()

    while True:
        success, frame = cap.read()
        if not success:
            break

        # 좌우 반전 (거울처럼 보이도록) - 단 좌표값도 left/right 변경해서 매칭해야함
        # frame = cv2.flip(frame, 1)
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        annotated_frame = frame.copy()
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                annotated_frame, # 그릴 대상 이미지 (BGR)
                results.pose_landmarks, # 포즈 추정 결과 (landmarks)
                mp_pose.POSE_CONNECTIONS, # 관절을 선으로 연결할 정의
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=2), # 랜드마크(점)의 스타일
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2) # 관절 연결선의 스타일
            )

            # 1초마다 요약 업데이트
            now = time.time()
            if now - last_update_time > 1:
                latest_pose_summary = summarize_pose(results.pose_landmarks.landmark)
                last_update_time = now
        else:
            latest_pose_summary = "포즈가 감지되지 않았습니다."

        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/pose_summary')
def pose_summary():
    return jsonify({"summary": latest_pose_summary})

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
    app.run(debug=True, host='0.0.0.0')
