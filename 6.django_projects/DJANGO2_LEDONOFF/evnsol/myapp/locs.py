from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json

def get_coordinates():
    landmarks = [
        {"name": "롯데월드타워", "lat": 37.5116, "lng": 127.0985},
        {"name": "63빌딩", "lat": 37.5195, "lng": 126.9402},
        {"name": "남산타워", "lat": 37.5512, "lng": 126.9883},
        {"name": "국립중앙박물관", "lat": 37.5231, "lng": 126.9807},
        {"name": "현충원", "lat": 37.5009, "lng": 126.9768},
        {"name": "고속터미널", "lat": 37.5045, "lng": 127.0042},
        {"name": "서울역", "lat": 37.5559, "lng": 126.9726},
        {"name": "LG트윈타워", "lat": 37.5108, "lng": 127.0589}
    ]

    return landmarks


@login_required
def loc_view(request):
    coordinates = get_coordinates()

    context = {
        'coordinates': coordinates
    }

    # print(coordinates)

    return render(request, 'map.html', context)
