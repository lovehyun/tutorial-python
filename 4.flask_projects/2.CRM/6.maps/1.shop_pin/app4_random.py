# http://127.0.0.1:5000/map/100
# http://127.0.0.1:5000/map/1000

from flask import Flask, render_template
import folium
from folium.plugins import MarkerCluster
import random

app = Flask(__name__)

# 서울 중심 좌표 (기준)
seoul_center = [37.5665, 126.9780]

# 대한민국 중심 좌표 (기준)
korea_center = [36.5, 127.5]

# 랜덤 좌표 생성 함수
def generate_random_coordinates(n):
    coordinates = []
    for _ in range(n):
        lat = random.uniform(37.4, 37.7)  # 서울시의 위도 범위
        lon = random.uniform(126.8, 127.1)  # 서울시의 경도 범위

        # lat = random.uniform(33.1, 38.6)  # 대한민국의 위도 범위
        # lon = random.uniform(125.1, 129.6)  # 대한민국의 경도 범위

        coordinates.append((lat, lon))
    return coordinates

# Folium 맵 생성 함수
def create_map(num_points):
    m = folium.Map(location=seoul_center, zoom_start=12)
    # m = folium.Map(location=korea_center, zoom_start=7)

    coordinates = generate_random_coordinates(num_points)

    marker_cluster = MarkerCluster().add_to(m)
    for coord in coordinates:
        folium.Marker(location=coord).add_to(marker_cluster)

    return m

@app.route('/map/<int:num_points>')
def map_view(num_points):
    m = create_map(num_points)
    map_html = m._repr_html_()
    return render_template('map.html', map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)
