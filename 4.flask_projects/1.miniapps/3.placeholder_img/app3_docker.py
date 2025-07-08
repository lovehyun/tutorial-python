from flask import Flask, request, send_file, render_template
from PIL import Image, ImageDraw, ImageFont
import io
import platform
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)  # 동적 URL 지원 (이 코드 내에서는 불필요, url_for 등 동적 url 미사용)

def get_font(font_size):
    try:
        system = platform.system()
        if system == "Windows":
            # Windows: 기본 Arial 폰트
            font = ImageFont.truetype("arial.ttf", font_size)
        else:
            # Linux: Noto Sans (패키지 설치 필요)
            font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf", font_size)
    except IOError:
        # 폰트 로딩 실패 시 기본 폰트 사용
        font = ImageFont.load_default()
    
    return font

def generate_placeholder_image(width, height, text, format='png'):
    image = Image.new('RGB', (width, height), color='gray')
    draw = ImageDraw.Draw(image)

    font_size = min(width, height) // 4
    font = get_font(font_size)

    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    draw.text((text_x, text_y), text, fill="white", font=font)

    img_byte_arr = io.BytesIO()

    # PNG 또는 JPEG 포맷에 따라 저장
    save_format = 'JPEG' if format in ['jpg', 'jpeg'] else 'PNG'
    image.save(img_byte_arr, format=save_format)
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

@app.route('/<int:width>x<int:height>.<format>')
def placeholder_image(width, height, format):
    text = f"{width}x{height}"
    format = format.lower()

    if format not in ['png', 'jpg', 'jpeg']:
        return "Unsupported format", 400

    # 이미지 생성
    image = generate_placeholder_image(width, height, text, format)

    mimetype = f'image/jpeg' if format in ['jpg', 'jpeg'] else 'image/png'
    return send_file(image, mimetype=mimetype)

if __name__ == '__main__':
    app.run(debug=True)
