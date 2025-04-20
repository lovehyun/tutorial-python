from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
import time
import atexit
import os
from dotenv import load_dotenv
import openai

# 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, static_folder='static')

# MediaPipe 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# 웹캠 초기화
cap = cv2.VideoCapture(0)
latest_pose_summary = "No pose detected yet."
latest_gpt_text = "자세 분석을 기다리는 중..."
last_api_call_time = 0  # API 호출 시간 추적

# OpenAI 클라이언트 초기화
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_pose(landmarks, frame_width=640, frame_height=480):
    """관절 좌표를 요약하고 정규화된 좌표와 픽셀 좌표로 변환"""
    key_joints = {
        # 상체 관절
        "left_shoulder": landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
        "right_shoulder": landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER],
        "left_elbow": landmarks[mp_pose.PoseLandmark.LEFT_ELBOW],
        "right_elbow": landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW],
        "left_wrist": landmarks[mp_pose.PoseLandmark.LEFT_WRIST],
        "right_wrist": landmarks[mp_pose.PoseLandmark.RIGHT_WRIST],
        # 손 관절
        "left_pinky": landmarks[mp_pose.PoseLandmark.LEFT_PINKY],
        "right_pinky": landmarks[mp_pose.PoseLandmark.RIGHT_PINKY],
        "left_index": landmarks[mp_pose.PoseLandmark.LEFT_INDEX],
        "right_index": landmarks[mp_pose.PoseLandmark.RIGHT_INDEX],
        "left_thumb": landmarks[mp_pose.PoseLandmark.LEFT_THUMB],
        "right_thumb": landmarks[mp_pose.PoseLandmark.RIGHT_THUMB],
        # 하체 관절
        "left_hip": landmarks[mp_pose.PoseLandmark.LEFT_HIP],
        "right_hip": landmarks[mp_pose.PoseLandmark.RIGHT_HIP],
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
    
    if visible_parts < 4:  # 최소 4개의 관절이 보여야 함
        return "주요 신체 부위가 충분히 감지되지 않았습니다. 전신이 보이도록 카메라 위치를 조정해주세요.", {}
    
    # GPT에 보낼 관절 데이터 (정규화된 좌표만)
    gpt_joints_data = {}
    for name, lm in key_joints.items():
        if lm.visibility > 0.5:
            gpt_joints_data[name] = {'x': float(f"{lm.x:.2f}"), 'y': float(f"{lm.y:.2f}"), 'visibility': float(f"{lm.visibility:.2f}")}
    
    return "\n".join(summary), gpt_joints_data


def get_gpt_feedback(joints_data):
    """OpenAI GPT에 포즈를 분석하도록 요청"""
    if not joints_data:
        return "충분한 관절 데이터가 없어 분석할 수 없습니다."
    
    prompt = f"""다음은 사람의 포즈에 대한 정규화된 좌표 데이터입니다:
{joints_data}

이 좌표 데이터를 바탕으로 사람의 자세나 위치를 간단하고 명확하게 한국어로 설명해주세요.
특히 팔의 위치(들었는지, 내렸는지, 앞이나 옆으로 뻗었는지)에 주목해서 설명해주세요.

가능하다면:
1. 현재 자세가 어떤 자세인지 (서있는지, 앉아있는지, 팔을 들고 있는지 등)
2. 양팔의 위치와 움직임 (왼팔/오른팔을 얼마나 들었는지, 방향은 어떤지)
3. 자세의 균형이나 정렬 상태

응답은 2-3문장으로 간결하게 해주세요."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # 또는 사용 가능한 다른 모델
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"GPT API 호출 오류: {e}")
        return f"자세 분석 중 오류가 발생했습니다: {str(e)[:100]}..."


def generate_frames():
    """비디오 프레임을 생성하고 포즈를 감지하여 분석"""
    global latest_pose_summary, latest_gpt_text, last_api_call_time
    
    while True:
        success, frame = cap.read()
        if not success:
            break

        # 좌우 반전 (거울처럼 보이도록) - 좌표값 좌우 바꿔서 할당해야함
        # frame = cv2.flip(frame, 1)
        
        # 프레임 크기 가져오기
        frame_height, frame_width = frame.shape[:2]
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        annotated_frame = frame.copy()
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                annotated_frame, 
                results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )

            # GPT 분석 업데이트 (5초마다)
            now = time.time()
            if now - last_api_call_time > 5:  # 5초마다 GPT API 호출
                pose_summary, joints_data = summarize_pose(results.pose_landmarks.landmark, frame_width, frame_height)
                latest_pose_summary = pose_summary
                
                if joints_data:  # 충분한 관절 데이터가 있을 때만 GPT 호출
                    latest_gpt_text = get_gpt_feedback(joints_data)
                    last_api_call_time = now
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
    return jsonify({
        "summary": latest_pose_summary,
        "description": latest_gpt_text
    })


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
