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
if not cap.isOpened():
    print("❌ 웹캠을 열 수 없습니다. 장치가 연결되어 있는지 확인해주세요.")
    exit(1)  # 프로그램 강제 종료

# 기본 설정 출력
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
fourcc_str = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])

print("웹캠 초기화 성공")
print(f"- 해상도: {int(width)} x {int(height)}")
print(f"- FPS: {fps:.2f}")
print(f"- FOURCC 코덱: {fourcc_str}")

latest_pose_summary = "No pose detected yet."


def analyze_pose(key_joints):
    feedback = []

    ls = key_joints["left_shoulder"]
    rs = key_joints["right_shoulder"]
    le = key_joints["left_elbow"]
    re = key_joints["right_elbow"]
    lw = key_joints["left_wrist"]
    rw = key_joints["right_wrist"]

    # 어깨 높이 차이
    shoulder_diff = abs(ls.y - rs.y)
    if shoulder_diff > 0.1:
        if ls.y > rs.y:
            feedback.append("왼쪽 어깨가 내려가 있습니다.")
        else:
            feedback.append("오른쪽 어깨가 내려가 있습니다.")
    else:
        feedback.append("어깨가 수평에 가깝습니다.")

    # 왼팔 위치 분석
    if le.y > ls.y and lw.y > le.y:
        feedback.append("왼팔이 아래로 내려가 있습니다.")
    elif le.y < ls.y and lw.y < le.y:
        feedback.append("왼팔을 들고 있습니다.")

    # 오른팔 위치 분석
    if re.y > rs.y and rw.y > re.y:
        feedback.append("오른팔이 아래로 내려가 있습니다.")
    elif re.y < rs.y and rw.y < re.y:
        feedback.append("오른팔을 들고 있습니다.")

    return feedback


def summarize_pose(landmarks, frame_width=640, frame_height=480):
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

    for name, lm in key_joints.items():
        if lm.visibility > 0.5:  # visibility 임계값 추가
            # 정규화된 좌표를 픽셀 좌표로 변환
            pixel_x = int(lm.x * frame_width)
            pixel_y = int(lm.y * frame_height)
            summary.append(f"{name}: 정규화({lm.x:.2f}, {lm.y:.2f}) / 픽셀({pixel_x}, {pixel_y})")
            visible_parts += 1
        else:
            summary.append(f"{name}: not visible")

    if visible_parts == 0:
        return "주요 신체 부위가 감지되지 않았습니다. 상반신이 보이도록 카메라 위치를 조정해주세요."

    # 자세 분석
    analysis = analyze_pose(key_joints)
    summary.append("\n[자세 분석]")
    summary.extend(analysis)

    return "\n".join(summary)


def generate_frames():
    global latest_pose_summary
    last_update_time = time.time()

    while True:
        success, frame = cap.read()
        if not success:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        annotated_frame = frame.copy()

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                annotated_frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )

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
    app.run(debug=True, use_reloader=False, host='0.0.0.0')
