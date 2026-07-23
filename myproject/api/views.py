import os
from dotenv import load_dotenv
import requests

from django.core.cache import cache

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


load_dotenv()
API_KEY = os.environ.get("API_KEY")


@api_view(["GET"])
def WeatherAPIWrapper(request):
    city = request.data["city"]
    if cache.get(city) != None: 
        return Response(cache.get(city))
    else:
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/?key={API_KEY}"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            today = data["days"][0]
            todayJson = {
                "city" : data["resolvedAddress"],
                "temp" : today["temp"],
                "temp_max" : today["tempmax"],
                "temp_min" : today["tempmin"],
                "climate_conditions" : today["conditions"],
                "description" : today["description"]
            }
            cache.set(key=city, value=todayJson, timeout=10)
            return Response(todayJson)
        return Response({"message" : "api request error"}, status=status.HTTP_502_BAD_GATEWAY)
