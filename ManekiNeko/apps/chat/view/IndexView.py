import json

from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from bot.model.response import Response, ResponseModelPartialFitting


@csrf_exempt
def index_response(request):
    if request.method == 'POST':
        sentence = json.loads(request.body.decode('utf-8'))
        sentence = sentence['body']

        res_model = Response()
        result = res_model.predict(sentence)
        result = "給我一下下, 我還在沉思！" if not result else result

        # re fitting
        # fit_model = ResponseModelPartialFitting()

        return HttpResponse(result)

