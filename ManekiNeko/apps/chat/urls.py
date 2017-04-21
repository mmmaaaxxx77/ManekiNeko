from django.conf.urls import url
from apps.chat.view import IndexView

urlpatterns = [
    url(r'^response/', IndexView.index_response),
]
