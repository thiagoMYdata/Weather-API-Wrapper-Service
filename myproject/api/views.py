from django.shortcuts import render
from django.http import HttpResponse

def firstSteps(requests):
    return HttpResponse("<h1>Hello World</h1>")

