# sudo apt-get install geoip-bin geoip-database
# geoiplookup 8.8.8.8
# pip install pygeoip

from flask import Flask, render_template, jsonify
import re
import os
import pygeoip

app = Flask(__name__)

# 로그 파일 경로
LOG_FILES = [
    '/var/log/nginx/access.log',
    '/var/log/nginx/access.log.1'
]

# GeoIP.dat 파일 로드
GEOIP_DB_PATH = '/usr/share/GeoIP/GeoIP.dat'
gi = pygeoip.GeoIP(GEOIP_DB_PATH)

# IP를 국가 코드로 변환하는 함수
def ip_to_country(ip):
    try:
        country = gi.country_name_by_addr(ip)
        return country
    except Exception as e:
        print(f"GeoIP lookup error for {ip}: {e}")
        return None

# access.log 파일 읽기
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

    locations = []
    for ip in ip_set:
        country = ip_to_country(ip)
        if country:
            locations.append({
                'ip': ip,
                'country': country
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
    app.run(host='0.0.0.0', port=5000, debug=True)
