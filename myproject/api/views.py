import os
from dotenv import load_dotenv
import requests

from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie 

from rest_framework.decorators import api_view
from rest_framework.response import Response

load_dotenv()
@cache_page(15)
@vary_on_cookie
@api_view(["GET"])
def apiTest(request):
    city = request.data["city"]
    api_key = os.environ.get("API_KEY")
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/?key={api_key}"
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
        return Response(todayJson)
