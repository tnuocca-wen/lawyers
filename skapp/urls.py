from .views import write, read, history
from django.urls import path

app_name = 'skapp'

urlpatterns = [
    path('history', history, name='history'),
    path('read/<slug:slug>', read, name='read'),
    path('', write, name='write')
]