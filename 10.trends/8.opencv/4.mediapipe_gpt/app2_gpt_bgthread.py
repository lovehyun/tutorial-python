from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
import time
import atexit
import os
from dotenv import load_dotenv
import openai
import threading
from datetime import datetime

# 환경 변수 로드 및 OpenAI 초기화
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__, static_folder='static')

# MediaPipe 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# 전역 변수
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[ERR] 웹캠을 열 수 없습니다.")
    exit(1)

latest_pose_summary = "No pose detected yet."
latest_gpt_text = "자세 분석을 기다리는 중..."
latest_gpt_based_on_time = None  # 분석 기준 시각 (포즈가 수집된 시각)
latest_joints_data = {}
last_api_call_time = 0


def summarize_pose(landmarks, frame_width=640, frame_height=480):
    global latest_joints_data, latest_gpt_based_on_time
    key_joints = {
        "left_shoulder": landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
        "right_shoulder": landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER],
        "left_elbow": landmarks[mp_pose.PoseLandmark.LEFT_ELBOW],
        "right_elbow": landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW],
        "left_wrist": landmarks[mp_pose.PoseLandmark.LEFT_WRIST],
        "right_wrist": landmarks[mp_pose.PoseLandmark.RIGHT_WRIST],
        "left_hip": landmarks[mp_pose.PoseLandmark.LEFT_HIP],
        "right_hip": landmarks[mp_pose.PoseLandmark.RIGHT_HIP],
    }

    summary = []
    visible_parts = 0
    joints_data = {}

    for name, lm in key_joints.items():
        if lm.visibility > 0.5:
            pixel_x = int(lm.x * frame_width)
            pixel_y = int(lm.y * frame_height)
            summary.append(f"{name}: 정규화({lm.x:.2f}, {lm.y:.2f}) / 픽셀({pixel_x}, {pixel_y})")
            visible_parts += 1
            joints_data[name] = {
                'x': float(f"{lm.x:.2f}"),
                'y': float(f"{lm.y:.2f}"),
                'visibility': float(f"{lm.visibility:.2f}")
            }
        else:
            summary.append(f"{name}: not visible")

    if visible_parts < 4:
        return "감지된 관절이 부족합니다.", {}

    latest_joints_data = joints_data
    latest_gpt_based_on_time = datetime.now()  # 이 시점의 포즈를 기준으로 GPT 분석하게 됨
    return "\n".join(summary), joints_data


def get_gpt_feedback(joints_data):
    prompt = f"""다음은 사람의 포즈에 대한 정규화된 좌표 데이터입니다:
{joints_data}

이 좌표 데이터를 바탕으로 사람의 자세나 위치를 간단하고 명확하게 한국어로 설명해주세요.
특히 팔의 위치(들었는지, 내렸는지, 앞이나 옆으로 뻗었는지)에 주목해서 설명해주세요.

가능하다면:
1. 현재 자세가 어떤 자세인지
2. 양팔의 위치와 움직임
3. 자세의 균형이나 정렬 상태

응답은 2-3문장으로 간결하게 해주세요."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"GPT API 오류: {e}")
        return f"분석 실패: {str(e)[:100]}"


def gpt_analysis_loop():
    global latest_joints_data, latest_gpt_text, last_api_call_time
    while True:
        time.sleep(1)
        if latest_joints_data and time.time() - last_api_call_time > 5:
            print(f"Query GPT...")
            latest_gpt_text = get_gpt_feedback(latest_joints_data)
            last_api_call_time = time.time()
            
            # 분석이 끝났으므로 이전 데이터 초기화
            latest_joints_data = {}


def generate_frames():
    global latest_pose_summary
    while True:
        success, frame = cap.read()
        if not success:
            print("[ERR] 프레임 읽기 실패")
            break

        frame_height, frame_width = frame.shape[:2]
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        annotated_frame = frame.copy()

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                annotated_frame, results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )
            summary, _ = summarize_pose(results.pose_landmarks.landmark, frame_width, frame_height)
            latest_pose_summary = summary
        else:
            latest_pose_summary = "포즈가 감지되지 않았습니다."

        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index2.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/pose_summary')
def pose_summary():
    based_on_time = latest_gpt_based_on_time.isoformat() if latest_gpt_based_on_time else None

    return jsonify({
        "summary": latest_pose_summary,
        "description": latest_gpt_text,
        "based_on_time": based_on_time
    })


@app.route('/shutdown')
def shutdown():
    cap.release()
    return "Camera Released"


@atexit.register
def release_camera_on_exit():
    if cap.isOpened():
        print("종료: 카메라 해제")
        cap.release()


if __name__ == '__main__':
    threading.Thread(target=gpt_analysis_loop, daemon=True).start()
    app.run(debug=True, use_reloader=False, host='0.0.0.0')
