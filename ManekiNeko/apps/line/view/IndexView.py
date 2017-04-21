#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from bot.model.response import Response, ResponseModelPartialFitting


line_bot_api = LineBotApi('EwNVmaOrfumzRmXE7S5Yh028ul5NFOxZXOvX7kr2moQp16/RgDLHcKWKDfUXGfiI/CzheL4v4VfS95qgO6mKt6D379uJoQ21kml59ik5MZcIUlW6cbG4VJSew3CjGHthkMluhg2ZKjspl8UOYyfqwQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0b908fe8f64b22183e2f2683823ef5ad')


def index_response(request):
    if request.method == 'GET':
        sentence = request.GET['q']
        res_model = Response()
        result = res_model.predict(sentence)
        result = "給我一下下, 我還在沉思！" if not result else result

        # re fitting
        # fit_model = ResponseModelPartialFitting()

        return HttpResponse(result)


def callback(request):
    if request.method == 'POST':
        signature = request.META['X-Line-Signature']

        line_request = request.body
        print(line_request)

        try:
            handler.handle(request.body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()

    return HttpResponse("OK")
