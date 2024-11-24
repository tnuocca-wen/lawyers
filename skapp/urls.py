from .views import write, read, index
from django.urls import path

app_name = 'skapp'

urlpatterns = [
    path('', index, name='index'),
    path('read/<slug:slug>', read, name='read'),
    path('write/', write, name='write')
]