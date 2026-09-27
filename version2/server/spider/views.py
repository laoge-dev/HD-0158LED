from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Message
from django.http.response import JsonResponse

# Create your views here.
def index(request):
    messages = Message.objects.all()
    output = []
    for message in messages:
        output.append({'title':message.title_text, 'mode':message.mode_int, 'g':message.green_text, 'r':message.red_text, 'date':message.pub_date, 'size':message.size_int})
    return JsonResponse(output, safe=False)

def detail(request, title):
    message = Message.objects.filter(title_text=title).first()
    output = {'error' : 'data not found.'}
    if message:
        output = {'title':message.title_text, 'mode':message.mode_int, 'g':message.green_text, 'r':message.red_text, 'date':message.pub_date, 'size':message.size_int}
    return JsonResponse(output)
