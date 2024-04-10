from django.urls import path

from . import views

app_name = 'DataVizLab'
urlpatterns = [
    path('', views.upload_csv, name='upload_csv'),            # ex: /Apps/DataVizLab/
]
