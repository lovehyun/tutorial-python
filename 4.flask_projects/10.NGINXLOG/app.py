from flask import Flask, render_template, jsonify
import re
import requests

app = Flask(__name__)

# IP를 위치(위도, 경도)로 변환
def ip_to_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,lat,lon", timeout=5)
        data = response.json()
        if data['status'] == 'success':
            return data['lat'], data['lon']
    except Exception as e:
        print(f"Error fetching location for {ip}: {e}")
    return None

# 로그 파일 읽기 + IP 추출
def parse_logs():
    log_files = ['access.log', 'access.log.1']
    ip_set = set()

    ip_pattern = re.compile(r'^(\d{1,3}(?:\.\d{1,3}){3})')

    for log_file in log_files:
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    match = ip_pattern.match(line)
                    if match:
                        ip_set.add(match.group(1))
        except FileNotFoundError:
            print(f"{log_file} not found. Skipping.")

    # IP 목록 → 위치 변환
    locations = []
    for ip in ip_set:
        loc = ip_to_location(ip)
        if loc:
            locations.append({
                'ip': ip,
                'lat': loc[0],
                'lon': loc[1]
            })
    return locations

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/api/locations')
def locations():
    data = parse_logs()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
