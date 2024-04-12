from django.urls import path

from . import views

app_name = 'DataVizLab'
urlpatterns = [
    path('', views.upload_excel, name='upload_excel'),            # ex: /Apps/DataVizLab/
    path('create_table/', views.create_table, name='create_table'),
]
