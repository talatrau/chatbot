from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, decorators
from django.contrib.auth.models import User

from chatbot.controller import getResponse, processMessage

# Create your views here.
@csrf_exempt
def answer(request):
    if request.method == 'POST':
        message = ""
        data = None
        user = request.POST['user']
        topic = request.POST['topic']

        if request.POST['message']:    
            message = request.POST['message']

        try:
            chunks = request.FILES['img'].chunks()
            data = next(chunks)
        except:
            pass

        processMessage(user, topic, message, data)

        return JsonResponse({})
    elif request.method == 'GET':
        answer = getResponse()
        return JsonResponse({'response': answer})


def getFashionChatHistory(request, user):
    if request.method == 'GET':
        data = []
        path = './chatbot/chat_history/fashion/' + user + '_history.txt'
        try:
            history = open(path, 'r', encoding='utf-8')
            data = history.read().split('\n')[:-1]
            history.close()
        except FileNotFoundError:
            history.close()
        finally:
            return JsonResponse({'response': data})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user is not None:
                #login(request, user)
                return JsonResponse({'user': username, 'state': 'success'})
            return JsonResponse({'user': username, 'state': 'failed'})
        except:
            return JsonResponse({'user': username, 'state': 'failed'})
    return JsonResponse({})