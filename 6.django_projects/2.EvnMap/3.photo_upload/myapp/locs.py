from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings

import os
import json


def get_coordinates():
    json_file_path = os.path.join(settings.BASE_DIR, 'locations.json')

    with open(json_file_path, encoding='utf-8') as file:
        landmarks = json.load(file)

    return landmarks


@login_required
def loc_view(request):
    coordinates = get_coordinates()

    context = {
        'coordinates': coordinates
    }

    # print(coordinates)

    return render(request, 'map.html', context)
