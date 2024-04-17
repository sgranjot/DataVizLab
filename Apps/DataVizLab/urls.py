from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'DataVizLab'
urlpatterns = [
    #path('', views.upload_excel, name='upload_excel'),            # ex: /Apps/DataVizLab/
    path('create_ExcelFile/', login_required(views.CreateExcelFileView.as_view()), name='create_ExcelFile'),
    #path('create_table/', views.create_table, name='create_table'),
    path('list_ExcelFiles/', login_required(views.ListExcelFileView.as_view()), name='list_ExcelFiles'),
    path('delete_ExcelFile/<int:pk>/', login_required(views.DeleteExcelFileView.as_view()), name='delete_ExcelFile'),
]
