from flask import Flask, render_template
import folium

app = Flask(__name__)

@app.route('/')
def index():
    # 커피샵 데이터
    coffee_shops = [
        {'name': 'Coffee Shop 1', 'latitude': 37.5665, 'longitude': 126.9780},
        {'name': 'Coffee Shop 2', 'latitude': 37.5651, 'longitude': 126.9778},
        {'name': 'Coffee Shop 3', 'latitude': 37.5673, 'longitude': 126.9765}
    ]

    # 지도 생성 (첫 번째 커피샵 좌표를 중심으로 설정)
    map_center = [coffee_shops[0]['latitude'], coffee_shops[0]['longitude']]
    mymap = folium.Map(location=map_center, zoom_start=15)

    # 마커 추가
    for shop in coffee_shops:
        folium.Marker(
            location=[shop['latitude'], shop['longitude']],
            popup=shop['name']
        ).add_to(mymap)

    # HTML로 저장
    map_html = mymap._repr_html_()
    # print(map_html)

    return render_template('index.html', map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)
