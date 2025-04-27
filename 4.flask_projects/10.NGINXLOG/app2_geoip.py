# sudo apt-get install geoip-bin geoip-database
# geoiplookup 8.8.8.8
# pip install geoip2

from flask import Flask, render_template, jsonify
import re
import os
import geoip2
import subprocess

app = Flask(__name__)

# 로그 파일 목록
LOG_FILES = [
    '/var/log/nginx/access.log',
    '/var/log/nginx/access.log.1'
]

# GeoIP.dat 파일 경로
GEOIP_DB_PATH = '/usr/share/GeoIP/GeoIP.dat'

# IP를 국가 이름으로 변환하는 함수
def ip_to_country(ip):
    try:
        # geoiplookup 명령어를 이용해 국가명 조회
        result = subprocess.run(['geoiplookup', ip], capture_output=True, text=True)
        output = result.stdout.strip()
        if 'GeoIP Country Edition' in output:
            parts = output.split(':')
            if len(parts) > 1:
                country_info = parts[1].strip()
                return country_info  # 예: US, United States
    except Exception as e:
        print(f"Error looking up IP {ip}: {e}")
    return None

# access.log 파일들을 읽고 IP 추출
def parse_logs():
    ip_set = set()
    ip_pattern = re.compile(r'^(\d{1,3}(?:\.\d{1,3}){3})')

    for log_file in LOG_FILES:
        if not os.path.exists(log_file):
            print(f"{log_file} not found. Skipping.")
            continue

        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    match = ip_pattern.match(line)
                    if match:
                        ip_set.add(match.group(1))
        except PermissionError:
            print(f"Permission denied: {log_file}")
        except Exception as e:
            print(f"Error reading {log_file}: {e}")

    # IP들을 국가로 변환
    results = []
    for ip in ip_set:
        country = ip_to_country(ip)
        if country:
            results.append({
                'ip': ip,
                'country': country
            })
    return results

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/api/locations')
def locations():
    data = parse_logs()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
