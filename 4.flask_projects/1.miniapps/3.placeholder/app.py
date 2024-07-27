from flask import Flask, request, send_file, render_template
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

# placeholder 이미지 생성 함수
def generate_placeholder_image(width, height, text):
    # 이미지 생성
    image = Image.new('RGB', (width, height), color='gray')
    draw = ImageDraw.Draw(image)
    
    # 폰트 설정
    font_size = min(width, height) // 4
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # 텍스트 크기 계산 및 이미지 중앙에 텍스트 배치
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    draw.text((text_x, text_y), text, fill="white", font=font)

    # 이미지 바이트로 변환
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return img_byte_arr

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        width = int(request.form['width'])
        height = int(request.form['height'])
        text = request.form['text']
        return send_file(generate_placeholder_image(width, height, text), mimetype='image/png')
    return render_template('index.html')

@app.route('/<int:width>x<int:height>.png')
def placeholder_image(width, height):
    text = f"{width}x{height}"
    return send_file(generate_placeholder_image(width, height, text), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
