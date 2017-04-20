import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from ManekiNeko.core.singleton.singleton import Singleton
from bot.model.response import Response


@login_required
def index(request):
    if request.method == 'GET':

        test = Test
        i = test.count(test)

        return render(request, 'dashboard/index.html', {'count': i})


@login_required
def index2(request):
    if request.method == 'GET':

        test = Test
        i = test.count(test)

        return render(request, 'dashboard/index.html', {'count': i})


@login_required
def index_response(request):
    if request.method == 'GET':
        sentence = request.GET['q']
        res_model = Response()
        result = res_model.predict(sentence)
        return HttpResponse(result)
        #return HttpResponse(json.dumps({'response': result}, ensure_ascii="False"), content_type="application/json; encoding=utf-8")
        #return JsonResponse({'response': result})


class Test(metaclass=Singleton):
    count2 = 0

    def __init__(self):
        self.count = 0

    def count(self):
        self.count2 += 1
        return self.count2
