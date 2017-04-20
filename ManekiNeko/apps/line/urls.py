from django.conf.urls import url
from apps.line.view import IndexView

urlpatterns = [
    url(r'^response/', IndexView.index_response),
    #url(r'^$', 'apps.dashboard.views.IndexView.index'),
]
